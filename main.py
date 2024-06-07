from app import App

def main():
    applications = App()
    applications.play()
    # applications.config()
    applications.window.mainloop()


if __name__ == '__main__':
    main()