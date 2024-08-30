import os
import ctypes
import msvcrt
from ctypes import wintypes
# FD / File Descriptor is a number a Operation system assigns to a file proccess to make it easier to identify the file

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
LOCKFILE_FAIL_IMMEDIATELY = 0x00000001
LOCKFILE_EXCLUSIVE_LOCK = 0x00000002
FILE_BEGIN = 0
F_GETFL = 3  # Get file descriptor flags
F_SETFL = 4  # Set file descriptor flags
FILE_ATTRIBUTE_READONLY = 0x00000001
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_FLAG_OVERLAPPED = 0x40000000

class OVERLAPPED(ctypes.Structure):
    _fields_ = [
        ("Internal", wintypes.ULONG),
        ("InternalHigh", wintypes.ULONG),
        ("Offset", wintypes.DWORD),
        ("OffsetHigh", wintypes.DWORD),
        ("hEvent", wintypes.HANDLE)
    ]

overlapped = OVERLAPPED()
overlapped.Offset = 0
overlapped.OffsetHigh = 0
overlapped.hEvent = ctypes.windll.kernel32.CreateEventW(None, True, False, None)
overlapped = ctypes.create_string_buffer(ctypes.sizeof(overlapped))


kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

GetFileAttributesW = kernel32.GetFileAttributesW
GetFileAttributesW.argtypes = [wintypes.LPCWSTR]
GetFileAttributesW.restype = wintypes.DWORD

SetFileAttributesW = kernel32.SetFileAttributesW
SetFileAttributesW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
SetFileAttributesW.restype = wintypes.BOOL

GetFinalPathNameByHandleW = kernel32.GetFinalPathNameByHandleW
GetFinalPathNameByHandleW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
GetFinalPathNameByHandleW.restype = wintypes.DWORD

CreateFileW = kernel32.CreateFileW
CreateFileW.argtypes = [
    wintypes.LPCWSTR,  # lpFileName
    wintypes.DWORD,    # dwDesiredAccess
    wintypes.DWORD,    # dwShareMode
    wintypes.LPVOID,   # lpSecurityAttributes
    wintypes.DWORD,    # dwCreationDisposition
    wintypes.DWORD,    # dwFlagsAndAttributes
    wintypes.HANDLE    # hTemplateFile
]
CreateFileW.restype = wintypes.HANDLE

LockFileEx = kernel32.LockFileEx
LockFileEx.argtypes = [
    wintypes.HANDLE,   # hFile
    wintypes.DWORD,    # dwFlags
    wintypes.DWORD,    # dwReserved
    wintypes.DWORD,    # nNumberOfBytesToLockLow
    wintypes.DWORD,    # nNumberOfBytesToLockHigh
    wintypes.LPVOID    # lpOverlapped
]
LockFileEx.restype = wintypes.BOOL

UnlockFileEx = kernel32.UnlockFileEx
UnlockFileEx.argtypes = [
    wintypes.HANDLE,   # hFile
    wintypes.DWORD,    # dwReserved
    wintypes.DWORD,    # nNumberOfBytesToUnlockLow
    wintypes.DWORD,    # nNumberOfBytesToUnlockHigh
    wintypes.LPVOID    # lpOverlapped
]
UnlockFileEx.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

DeviceIoControl = kernel32.DeviceIoControl
DeviceIoControl.argtypes = [
    wintypes.HANDLE,   # hDevice
    wintypes.DWORD,    # dwIoControlCode
    wintypes.LPVOID,   # lpInBuffer
    wintypes.DWORD,    # nInBufferSize
    wintypes.LPVOID,   # lpOutBuffer
    wintypes.DWORD,    # nOutBufferSize
    wintypes.LPDWORD,  # lpBytesReturned
    wintypes.LPVOID    # lpOverlapped
]
DeviceIoControl.restype = wintypes.BOOL

def check_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

LockFileEx.errcheck = check_bool
UnlockFileEx.errcheck = check_bool

LOCK_SH = 0x01  
LOCK_EX = 0x02  
LOCK_UN = 0x08  
LOCK_NB = 0x04  



def fcntl(fd, cmd, arg=0):
        """Implements fcntl functionality for file control on Windows."""
        # Convert file descriptor to file path
        file_path = os.path.abspath(fd_to_path(fd))
        
        if cmd == F_GETFL:
            # Get file attributes using Windows API
            attrs = GetFileAttributesW(file_path)
            if attrs == 0xFFFFFFFF:
                raise ctypes.WinError(ctypes.get_last_error())

            # Translate the attributes to flags
            if attrs & FILE_ATTRIBUTE_READONLY:
                return os.O_RDONLY
            else:
                return os.O_RDWR

        elif cmd == F_SETFL:
            # Set file attributes using Windows API
            if arg & os.O_RDONLY:
                success = SetFileAttributesW(file_path, FILE_ATTRIBUTE_READONLY)
            elif arg & os.O_RDWR:
                success = SetFileAttributesW(file_path, FILE_ATTRIBUTE_NORMAL)
            else:
                raise ValueError("Unsupported flag for F_SETFL.")
            
            if not success:
                raise ctypes.WinError(ctypes.get_last_error())

            return 0

        else:
            raise ValueError(f"Command {cmd} not supported.")



def fd_to_path(fd):
        """Convert file descriptor to file path on Windows."""
        handle = msvcrt.get_osfhandle(fd)
        
        if handle == INVALID_HANDLE_VALUE:
            raise ctypes.WinError(ctypes.get_last_error())

        buffer_size = os.path.getsize(path_buffer.value)
        path_buffer = ctypes.create_unicode_buffer(buffer_size)

        result = GetFinalPathNameByHandleW(handle, path_buffer, buffer_size, 0)

        if result == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        return path_buffer.value

def flock(fd, operation):
        handle = msvcrt.get_osfhandle(fd)
        """Mimics flock for file locking."""
        if operation & LOCK_UN:
            UnlockFileEx(handle, 0, 0xFFFFFFFF, 0xFFFFFFFF, None)
        else:
            flags = 0
            if operation & LOCK_EX:
                flags |= LOCKFILE_EXCLUSIVE_LOCK
            if operation & LOCK_NB:
                flags |= LOCKFILE_FAIL_IMMEDIATELY
            LockFileEx(handle, flags, 0, 0xFFFFFFFF, 0xFFFFFFFF, None)

def ioctl(fd, request, arg=0):
        handle = msvcrt.get_osfhandle(fd)
        """Mimics ioctl functionality for device-specific operations."""

        out_buffer = os.path.getsize(fd_to_path(fd))
        bytes_returned = wintypes.DWORD(0)
        success = DeviceIoControl(
            handle,
            request,
            ctypes.byref(ctypes.c_int(arg)),
            ctypes.sizeof(ctypes.c_int),
            out_buffer,
            ctypes.sizeof(out_buffer),
            ctypes.byref(bytes_returned),
            None
        )
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        return out_buffer.raw[:bytes_returned.value]
     

def close(fd):
        handle = msvcrt.get_osfhandle(fd)
        """Closes the file handle."""
        if handle:
            CloseHandle(handle)
            handle = None

