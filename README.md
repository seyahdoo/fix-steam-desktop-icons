# Steam Desktop Shortcut Icon Fixer

A specialized tool designed to repair broken or missing Steam game icons on your Windows desktop by automatically downloading them from Steam's CDN.

## 🚀 Features
- **Automatic Detection**: Scans multiple desktop locations for Steam `.url` shortcuts.
- **Steam Integration**: Automatically locates your Steam installation via the Windows Registry.
- **Smart Downloading**: Retrieves missing icons directly from Steam's official CDN.
- **Customizable**: Supports custom desktop paths via a simple JSON configuration.
- **Grouped Logging**: Provides clean, grouped English logs for better traceability.

---

## 🛠️ Usage Instructions

1. **Standard Run**: 
   - Simply run `main.py` (or the compiled `.exe`).
   - The tool will automatically check your default Desktop and OneDrive Desktop.
2. **Custom Path**: 
   - Create a file named `custom_location.json` in the same directory as the program.
   - Add your desktop path (see the [Custom Path Section](#custom-path-configuration) below).
3. **Completion**: 
   - Once finished, right-click your desktop and select **Refresh** to load the newly downloaded icons.
   - The program will wait for you to press **Enter** before closing, ensuring you can review the results.

---

## 🧠 Logic Flow & Decision Making

The application follows a **Research -> Analysis -> Execution** lifecycle based on Clean Architecture:

### 1. Path Discovery (Decision Logic)
The program determines which directories to scan for shortcuts based on the following priority:
- **Priority 1 (Override)**: Check if `custom_location.json` exists and contains a **valid, existing directory** in the `desktop_path` field. If valid, it scans **ONLY** this path.
- **Priority 2 (Fallback)**: If no valid custom path is found, it attempts to check system default paths:
    - `%USERPROFILE%\Desktop`
    - `%USERPROFILE%\OneDrive\Desktop`
- **Validation**: All attempted paths are logged. Only paths that actually exist on your disk are processed.

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

## 📂 Custom Path Configuration

To scan a specific folder (e.g., a secondary drive's desktop), create `custom_location.json`:

```json
{
    "desktop_path": "D:\\Users\\ExampleUser\\Desktop"
}
```
> **Note**: Use double backslashes `\\` for Windows paths to avoid JSON formatting errors.

---

## ❓ Q&A Section

### Q: Why does the log say "No valid custom path found"?
**A:** This happens if `custom_location.json` is missing, or if the path provided inside it does not exist on your computer. The program will safely fallback to your default Windows desktop.

### Q: What is a "Formatting Error" in the config file?
**A:** This refers to invalid JSON syntax, such as:
- Using single quotes (`'`) instead of double quotes (`"`).
- Forgetting to escape backslashes (e.g., using `C:\Path` instead of `C:\\Path`).
- Missing the required `"desktop_path"` key name.

### Q: Does this tool modify my shortcut files?
**A:** No. The tool only reads your shortcuts to find out which icons are missing and then places the missing `.ico` files into your Steam installation folder where Windows expects them to be.

### Q: The program finished, but I still don't see the icons.
**A:** Windows often caches icons. Right-click an empty space on your desktop and click **Refresh**. If that fails, restarting `explorer.exe` or your PC will force a refresh.

### Q: Why is the program waiting for "Press Enter to exit"?
**A:** This is by design. It prevents the terminal window from closing immediately so you can read the logs and confirm which icons were successfully repaired.
