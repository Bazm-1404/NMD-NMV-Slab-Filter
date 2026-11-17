# NMD / NMV Slab Filtering Application — Windows build

This package prepares your existing Tkinter application for building on a GitHub-hosted Windows runner.
The resulting application is a folder-based Windows build (`--onedir`), not a single-file EXE.

## Before uploading

1. Confirm that your company permits this source code to be stored in GitHub, even in a **private** repository.
2. If it is company-owned or contains internal logic/data, obtain approval first.
3. Do not upload any real customer data or telecom input files.

## Create the GitHub repository

1. Sign in to GitHub.
2. Create a new repository named `NMD-NMV-Slab-Filter`.
3. Set visibility to **Private**.
4. Do not initialize it with a README, license, or `.gitignore`.
5. Upload the contents of this package to the repository. The `.github/workflows/build-windows.yml`
   file must retain its folder structure.

## Start the build

1. Open the repository on GitHub.
2. Select the **Actions** tab.
3. Open **Build Windows EXE**.
4. Select **Run workflow**, then confirm **Run workflow**.
5. Wait for the workflow to finish successfully.
6. Open the completed workflow run. Under **Artifacts**, download
   `NMD_NMV_Slab_Filter_Windows`.
7. Extract the downloaded ZIP. Run `NMD_NMV_Slab_Filter.exe` inside the extracted
   `NMD_NMV_Slab_Filter` folder.

Keep the entire extracted folder together; the EXE depends on files alongside it.

## Important security note

GitHub Actions builds the program on a hosted Windows machine. It does not guarantee that
your company's antivirus will accept the resulting application. Do not disable antivirus
or bypass company security controls. If it is detected, provide the detection name and build
details to your IT/security team for review.

The workflow runs automatically on pushes to `main`, and can also be started manually
from the Actions tab. Build artifacts are retained for 14 days.
