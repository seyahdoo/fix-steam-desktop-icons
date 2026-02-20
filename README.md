# Steam Desktop Shortcut Icon Fixer

A specialized tool designed to repair broken or missing Steam game icons on your Windows desktop by automatically downloading them from Steam's CDN.

## 🚀 Features
- **Automatic Detection**: Smartly identifies your Desktop location via Windows Registry and standard paths.
- **Steam Integration**: Automatically locates your Steam installation via the Windows Registry.
- **Smart Downloading**: Retrieves missing icons directly from Steam's official CDN.
- **Grouped Logging**: Provides clean, grouped English logs for better traceability.

---

## 🛠️ Usage Instructions

1. **Run the Tool**: 
   - Simply run `main.py` (or the compiled `.exe`).
   - The tool will automatically detect your Desktop folder (including OneDrive or custom locations set in Windows).
2. **Completion**: 
   - Once finished, right-click your desktop and select **Refresh** to load the newly downloaded icons.
   - The program will wait for you to press **Enter** before closing, ensuring you can review the results.

---

## 🧠 Logic Flow & Decision Making

The application follows a **Research -> Analysis -> Execution** lifecycle based on Clean Architecture:

### 1. Path Discovery (Decision Logic)
The program determines which directories to scan for shortcuts using a robust multi-step approach:
- **Registry Lookup**: Queries `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders` to find the current user's authoritative Desktop path.
- **Standard Fallbacks**: Also checks standard locations (`%USERPROFILE%\Desktop` and `%USERPROFILE%\OneDrive\Desktop`) to ensure no shortcuts are missed.
- **Validation**: All unique, existing paths are aggregated and scanned.

### 2. Shortcut Parsing
- Scans target directories for `.url` files.
- Each file is parsed to extract:
    - **Game ID**: From the `URL=steam://rungameid/...` line.
    - **Icon Hash**: From the `IconFile=...` line (e.g., `abc123...ico`).

### 3. Icon Verification & Repair
- Locates the Steam installation folder (via Registry or default `C:\Program Files (x86)\Steam`).
- Checks the `Steam\steam\games` folder for the required `.ico` files.
- **Decision**: If the icon is missing, it constructs a download URL using the Game ID and Icon Hash and retrieves it from Steam's CDN.

---

## ❓ Q&A Section

### Q: Does this tool modify my shortcut files?
**A:** No. The tool only reads your shortcuts to find out which icons are missing and then places the missing `.ico` files into your Steam installation folder where Windows expects them to be.

### Q: The program finished, but I still don't see the icons.
**A:** Windows often caches icons. Right-click an empty space on your desktop and click **Refresh**. If that fails, restarting `explorer.exe` or your PC will force a refresh.

### Q: Why is the program waiting for "Press Enter to exit"?
**A:** This is by design. It prevents the terminal window from closing immediately so you can read the logs and confirm which icons were successfully repaired.
