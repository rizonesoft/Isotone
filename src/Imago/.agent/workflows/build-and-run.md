---
description: Build and run Imago to test changes
---

# Build and Run Imago

Use this workflow after making code changes to test them.

## Steps

// turbo
1. Build the solution:
```powershell
dotnet build Imago.sln --no-restore -v q
```

// turbo
2. Run the application:
```powershell
dotnet run --project src/Imago.UI
```

3. Test the changes manually in the running application.

4. When done testing, close the application window.
