# (col, label, base, fn) ; この1本のリストから map と bindings を両方生成する
ROWS = [
 [(0,"Esc","&kp ESC","&trans"),(1,"1","&kp N1","&kp F1"),(2,"2","&kp N2","&kp F2"),(3,"3","&kp N3","&kp F3"),
  (4,"4","&kp N4","&kp F4"),(5,"5","&kp N5","&kp F5"),(6,"6","&kp N6","&kp F6"),(7,"7","&kp N7","&kp F7"),
  (8,"8","&kp N8","&kp F8"),(9,"9","&kp N9","&kp F9"),(10,"0","&kp N0","&kp F10"),(11,"-","&kp MINUS","&kp F11"),
  (12,"^","&kp EQUAL","&kp F12"),(13,"\\","&kp INT3","&trans"),(14,"Del","&kp DEL","&trans")],
 [(0,"Tab","&kp TAB","&trans"),(1,"Q","&kp Q","&bt BT_SEL 0"),(2,"W","&kp W","&bt BT_SEL 1"),(3,"E","&kp E","&bt BT_SEL 2"),
  (4,"R","&kp R","&trans"),(5,"T","&kp T","&trans"),(6,"Y","&kp Y","&trans"),(7,"U","&kp U","&trans"),
  (8,"I","&kp I","&trans"),(9,"O","&kp O","&trans"),(10,"P","&kp P","&trans"),(11,"@","&kp LBKT","&trans"),
  (12,"[","&kp RBKT","&trans"),(13,"Back","&kp BSPC","&bt BT_CLR")],
 [(0,"Caps","&kp CAPS","&trans"),(1,"A","&kp A","&trans"),(2,"S","&kp S","&trans"),(3,"D","&kp D","&trans"),
  (4,"F","&kp F","&trans"),(5,"G","&kp G","&trans"),(6,"H","&kp H","&trans"),(7,"J","&kp J","&trans"),
  (8,"K","&kp K","&trans"),(9,"L","&kp L","&trans"),(10,";","&kp SEMI","&trans"),(11,":","&kp QUOT","&trans"),
  (12,"]","&kp NUHS","&trans"),(13,"Enter","&kp RET","&trans")],
 [(0,"LShift","&kp LSHFT","&trans"),(1,"Z","&kp Z","&out OUT_USB"),(2,"X","&kp X","&out OUT_BLE"),(3,"C","&kp C","&trans"),
  (4,"V","&kp V","&trans"),(5,"B","&kp B","&trans"),(6,"N","&kp N","&trans"),(7,"M","&kp M","&trans"),
  (8,",","&kp COMMA","&trans"),(9,".","&kp DOT","&trans"),(10,"/","&kp FSLH","&trans"),(11,"_","&kp INT1","&trans"),
  (12,"Up","&kp UP","&kp PG_UP"),(13,"RShift","&kp RSHFT","&trans")],
 [(0,"LCtrl","&kp LCTRL","&trans"),(1,"Fn","&mo 1","&trans"),(2,"Win","&kp LGUI","&trans"),(3,"LAlt","&kp LALT","&trans"),
  (4,"Space","&kp SPACE","&trans"),(11,"RCtrl","&kp RCTRL","&trans"),(12,"Left","&kp LEFT","&kp HOME"),
  (13,"Down","&kp DOWN","&kp PG_DN"),(14,"Right","&kp RIGHT","&kp END")],
]
EXP=[15,14,14,14,9]
for r,row in enumerate(ROWS):
    cols=[c for c,*_ in row]
    assert len(row)==EXP[r], (r,len(row))
    assert cols==sorted(set(cols)) and all(0<=c<=14 for c in cols)
def pad(s,w): return s+" "*(w-len(s))
def block(fn, ind):
    out=[]
    for r,row in enumerate(ROWS):
        out.append(ind+"// R%d: "%r+" ".join(l for _,l,_,_ in row))
        out.append(ind+" ".join(fn(r,e) for e in row))
    return "\n".join(out)
open("map.txt","w").write(block(lambda r,e:"RC(%d,%d)"%(r,e[0]),"            "))
open("base.txt","w").write(block(lambda r,e:e[2],"                "))
open("fn.txt","w").write(block(lambda r,e:e[3],"                "))
print("OK total",sum(map(len,ROWS)))
