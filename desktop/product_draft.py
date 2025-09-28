class ProductDraft():
    def __init__(self):
        self.ref_num = None
        self.name = None
        self.barcode = None
        self.pcs_innerbox = None
        self.pcs_ctn = None
        self.weight = None
        self.price_usd = None
        self.price_rmb = None
        self.remarks = None
        self.packing = None
        self.customers = []
        self.quotes = []
        self.imgs = []
        self.tags = []

    @classmethod
    def from_vm(cls, vm):
        draft = cls()
        draft.ref_num = vm.ref_num
        draft.name = vm.name
        draft.barcode = vm.barcode
        draft.pcs_innerbox = vm.pcs_innerbox
        draft.pcs_ctn = vm.pcs_ctn
        draft.weight = vm.weight
        draft.price_usd = vm.price_usd
        draft.price_rmb = vm.price_rmb
        draft.remarks = vm.remarks
        draft.packing = vm.packing
        draft.customers = list(vm.customers)
        draft.quotes = [q.copy() for q in vm.quotes]
        draft.imgs = [img["img"] if isinstance(img, dict) else img for img in vm.imgs]
        draft.tags = list(vm.tags)
        return draft
    
    def to_payload(self) -> dict:
        return {
            "ref_num": self.ref_num,
            "name": self.name,
            "barcode": self.barcode,
            "pcs_innerbox": self.pcs_innerbox,
            "pcs_ctn": self.pcs_ctn,
            "weight": self.weight,
            "price_usd": self.price_usd,
            "price_rmb": self.price_rmb,
            "remarks": self.remarks,
            "packing": self.packing,
            "customers": list(self.customers),
            "quote": [q.copy() for q in self.quotes],
            "imgs": list(self.imgs),
            "tags": list(self.tags),
            "locked_by": None,
            "locked_timestamp": None,
            "last_updated": None,
        }
