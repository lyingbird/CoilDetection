# object information

class OBJ:
    def __init__(self):
        self.names = [
                    # "bronze",
                    # "bulb",
                    "candy box",
                    "clip",
                    # "coin",
                    # "fork",
                    # "knife",
                    # "key",
                    # "lighter",
                    # "pen",
                    # "ring",
                    # "scissor",
                    # "spoon",
                    "iphone front",
                    "iphone back",
                    # "two tapes",
                    # "three tapes",
                    # "staple",
                    # "CD driver",
                    # "clip big",
                    # "cola",
                    # "disk",
                    # "nexus back",
                    "nexus front",
                    # "ruler",
                    # "spray",
                    # "torch",
                    # "wrench",

                    # "buckle",
                    "converter",
                    # "expo",
                    # "five cents",
                    # "gear",
                    # "metal pen", #`
                    # "one cent",
                    "one dime",
                    # "quarter",
                    # "utility tool Cshape",
                    # "utility tool Lshape",
                    # "wrenchA",
                    # "wrenchB",
                    "credit card",
                    "accessory",     #
                    "scissor big",
                    # "nexus5 back",
                    # "nexus5 back with copper tape",
                    "scissor big with copper tape",
                    "candy box with copper tape",
                    # "nexus back with copper tape",
                    "book1",
                    "book2",
                    "book3",
                    "knife2",
                    "knife2 with copper tape",
                    "book4",
                    "book5",
                    "kindle front",
                    # "kindle back",
                    # "disk with copper tape",
                    "finger",
                    # "nailclipper",
                    "USB",
                    # "tinfoil",
                    # "nailclipper with copper tape",
                    # "screwdriver",
                    "bottle cap",
                ]

        self.id = {
                    # "bronze"     :0,
                    # "bulb"       :1,  # NOTE
                    "candy box"  :2,
                    "clip"       :3,
                    # "coin"       :4,
                    "fork"       :5,
                    "knife"      :6,
                    "key"        :7,
                    # "lighter"    :8,
                    # "pen"        :9,
                    "ring"       :10,
                    "scissor"    :11,
                    "spoon"      :12,
                    "iphone front"   :13,
                    "iphone back"    :14,
                    # "two tapes"      :15,
                    # "three tapes"    :16,
                    # "staple          :17"
                    # "CD driver"      :18,
                    "clip big"       :19,
                    # "cola"           :20,
                    "disk"           :21,
                    "nexus back"      :22,
                    "nexus front"     :23,
                    # "ruler"          :24,
                    # "spray"          :25,
                    # "torch"          :26,
                    # "wrench"         :27,

                    # "buckle"         :28,
                    "converter"      :29,
                    ###########################################
                    "expo"           :30,
                    "five cents"     :31,
                    # "gear"           :32,
                    "metal pen"      :33,
                    "one cent"       :34,
                    "one dime"       :35,
                    "quarter"        :36,
                    # "utility tool Cshape"  :37,
                    # "utility tool Lshape"  :38,
                    "wrenchA"        :39,
                    "wrenchB"        :40,
                    "credit card"    :41,
                    "accessory"      :42,
                    "scissor big"    :43,
                    # "nexus5 back"                :44,
                    # "nexus5 back with copper tape"   :45,
                    "scissor big with copper tape"   :46,
                    "candy box with copper tape"     :47,
                    # "nexus back with copper tape"    :48,
                    "book1"    :49,
                    "book2"    :50,
                    "book3"    :51,
                    "knife2"   :52,
                    "knife2 with copper tape"        :53,
                    "book4"    :54,
                    "book5"    :55,
                    "kindle front"   :56,
                    # "kindle back"    :57,
                    # "disk with copper tape"    :58,
                    "finger"                   :59,
                    # "nailclipper"              :60,
                    "USB"                      :61,
                    # "tinfoil"                  :62,
                    # "nailclipper with copper tape"  :63,
                    "screwdriver"              :64,
                    "bottle cap"               :65,
                }

    # @staticmethod
    def find(self, obj):
        if obj in self.names:
            return True
        else:
            return False

    # @staticmethod
    def obj_id(self, obj):
        return self.id[obj]
