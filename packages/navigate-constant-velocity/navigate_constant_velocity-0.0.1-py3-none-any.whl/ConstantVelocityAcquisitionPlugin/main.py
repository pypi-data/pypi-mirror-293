import tkinter
from view.constant_velocity_acquisition_frame import ConstantVelocityAcquisitionFrame

def main():
    print("starting plugin name!")

    # show the view
    root = tkinter.Tk()
    frame = ConstantVelocityAcquisitionFrame(root)
    frame.grid(column=0, row=0)
    root.mainloop()


if __name__ == "__main__":
    main()