import os.path
import site

# https://github.com/simonflueckiger/tesserocr-windows_build/issues/28
site_packages_dir = site.getsitepackages()[1]
pyqt5_msvcp140_fp = os.path.join(site_packages_dir, "PyQt5", "Qt5", "bin",
                                 "msvcp140.dll")
if os.path.isfile(pyqt5_msvcp140_fp):
    os.remove(pyqt5_msvcp140_fp)
