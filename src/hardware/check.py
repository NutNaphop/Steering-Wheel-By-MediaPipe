import vgamepad as vg

gamepad = vg.VX360Gamepad()
print("Controller created! เปิด joy.cpl ได้เลย...")
input("กด Enter เพื่อออก")
gamepad.reset()