import pyray
import Managers

def main():
    pyray.set_target_fps(60)
    appManager = Managers.AppManager()

    appManager.Initialization()
    while not pyray.window_should_close():
        appManager.Update()
        appManager.Draw()
    pyray.close_window()


if __name__ == '__main__':
    main()