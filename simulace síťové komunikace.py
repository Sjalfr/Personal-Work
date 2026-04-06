import re
from abc import ABC, abstractmethod

class PDU(ABC):
    def __init__(self, payload: str):
        # Protekce proti vytvoření instance PDU přímo
        if type(self) is PDU:
            raise TypeError("Nelze vytvořit instanci abstraktní třídy PDU.")
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @abstractmethod
    def isValid(self) -> bool:
        pass


class EthFrame(PDU):
    def __init__(self, dmac: str, smac: str, eth_type: int, payload: str, fcs: int = None):
        super().__init__(payload)
        
        # Validace MAC hned při vzniku
        if not self.isValidMac(dmac) or not self.isValidMac(smac):
            raise ValueError("Neplatný formát MAC adresy.")
            
        self.__dmac = dmac
        self.__smac = smac
        self.__type = eth_type
        
        # Pokud fcs není zadáno, spočítáme ho
        self.__fcs = fcs if fcs is not None else self._calculateFcs()

    @staticmethod
    def isValidMac(mac: str) -> bool:
        pattern = r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"
        return bool(re.match(pattern, mac))

    def _calculateFcs(self) -> int:
        raw_data = f"{self.__dmac}{self.__smac}{self.__type}{self.payload}"
        hash_val = 0
        for char in raw_data:
            # Trocha bitových operací, aby to nevypadalo primitivně
            hash_val = ((hash_val << 5) - hash_val) + ord(char)
            hash_val &= 0xFFFFFFFF  # Omezení na 32-bit integer
        return hash_val

    def _recalculate(self):
        self.__fcs = self._calculateFcs()

    # --- Gettery a Settery s logikou ---
    @property
    def dmac(self): return self.__dmac

    @dmac.setter
    def dmac(self, val):
        if self.isValidMac(val):
            self.__dmac = val
            self._recalculate()

    @property
    def payload(self): return self._payload

    @payload.setter
    def payload(self, val):
        self._payload = val
        self._recalculate()  # Override setteru z rodiče s auto-hash

    @property
    def fcs(self): return self.__fcs

    def isValid(self) -> bool:
        return self.__fcs == self._calculateFcs()

    def corruptData(self):
        self._payload = "ERR_DATA_CORRUPTED"
        # Úmyslně nenastavíme recalculate, fcs zůstane staré
        self.__fcs = 999999 

    def __str__(self):
        return f"[EthFrame] DST: {self.__dmac} | SRC: {self.__smac} | TYPE: {hex(self.__type)} | FCS: {self.__fcs}"

# --- Rychlá ukázka funkčnosti ---
if __name__ == "__main__":
    frame = EthFrame("00:1A:2B:3C:4D:5E", "AA:BB:CC:DD:EE:FF", 0x0800, "SecretData")
    print(frame)
    print(f"Je rámec v pořádku? {frame.isValid()}")
    
    frame.corruptData()
    print("Po poškození:", frame)
    print(f"Je rámec stále v pořádku? {frame.isValid()}")