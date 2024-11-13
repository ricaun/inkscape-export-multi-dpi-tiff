# Release Extension

To release the extension in the [inkscape extensions](https://inkscape.org/develop/extensions/) is necessary to sign the `zip` file with `GPG` or `MD5`.

This project use `MD5` to be simpler to implement.

First is necessary to enable the checksums in the user profile, just add some text to activate the upload validation feature.

![image](https://github.com/user-attachments/assets/aa17e182-0b73-476a-8961-d0d806447c31)

## Windows

To create the `MD5` checksums in windows the code below is used in the `zip` file.

```cmd
powershell -Command "Get-FileHash -Path 'export_multi_page_tiff.zip' -Algorithm MD5 | Select-Object -ExpandProperty Hash | ForEach-Object { $_.ToLower() + '  ' + 'export_multi_page_tiff.zip' } | Out-File -FilePath 'export_multi_page_tiff.md5' -encoding ascii"
```

This generate the `export_multi_page_tiff.md5` to be uploaded with the `zip` file in the [inkscape extensions](https://inkscape.org/develop/extensions/)

![image](https://github.com/user-attachments/assets/22121477-cdad-47f3-81bf-181ec75aa508)


## Release Automation

The [release.cmd](release.cmd) file create the `zip` file using the `export_multi_page_tiff` folder and create the `md5` checksums for the `zip` file.

The files is created inside the `Release` folder.

---
