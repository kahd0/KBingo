def centralizeWindow(window, width, height):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth - width) // 2
    y = (screenHeight - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
