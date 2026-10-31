import struct
from typing import Dict, List, Any, Generator, Tuple


class BitFieldEntityProcessor:
    """Packs and unpacks spatial entity tick data into packed bitfields for low-latency gaming sync."""

    # Payload schema: header (16-bit: health 8b, team 4b, flags 4b) + norm_x (16-bit) + norm_y (16-bit)
    PACK_FORMAT = ">HHH"

    def __init__(self, map_bounds: Tuple[float, float] = (1024.0, 1024.0)):
        self.max_x, self.max_y = map_bounds

    def pack_entity(self, health: int, team: int, flags: int, x: float, y: float) -> bytes:
        """Quantizes position floats and packs metadata into a compact 6-byte payload."""
        norm_x = int(min(max(x, 0.0), self.max_x) / self.max_x * 65535)
        norm_y = int(min(max(y, 0.0), self.max_y) / self.max_y * 65535)
        
        header = ((health & 0xFF) << 8) | ((team & 0x0F) << 4) | (flags & 0x0F)
        return struct.pack(self.PACK_FORMAT, header, norm_x, norm_y)

    def unpack_entity(self, payload: bytes) -> Dict[str, Any]:
        """Expands 6-byte packed state back into readable entity dict."""
        header, norm_x, norm_y = struct.unpack(self.PACK_FORMAT, payload)
        
        return {
            "health": (header >> 8) & 0xFF,
            "team": (header >> 4) & 0x0F,
            "flags": header & 0x0F,
            "x": round((norm_x / 65535.0) * self.max_x, 2),
            "y": round((norm_y / 65535.0) * self.max_y, 2),
        }

    def stream_deltas(self, baseline: List[bytes], current: List[bytes]) -> Generator[Tuple[int, bytes], None, None]:
        """Yields entity index and payload for states modified since last server tick."""
        for idx, (old_frame, new_frame) in enumerate(zip(baseline, current)):
            if old_frame != new_frame:
                yield idx, new_frame


def calculate_tick_checksum(payloads: List[bytes]) -> int:
    """Calculates FNV-1a 32-bit hash across active entity byte payloads for tick verification."""
    checksum = 0x811C9DC5
    for chunk in payloads:
        for byte in chunk:
            checksum = ((checksum ^ byte) * 0x01000193) & 0xFFFFFFFF
    return checksum
