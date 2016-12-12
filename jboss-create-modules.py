# Sachindra Dasun <sachindradasun@gmail.com>
#
# Create JBoss Modules for jar files
#
# This python script can be used to create JBoss modules with module.xml for jar files.
# This script is useful when migrating to JBoss AS 7

import os
import zipfile
import shutil

# Content for module.xml file
MODULE_XML = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" \
             "<module xmlns=\"urn:jboss:module:1.1\" name=\"{}\">\n" \
             "\t<resources>\n" \
             "\t\t<resource-root path=\"{}\"/>\n" \
             "\t</resources>\n" \
             "</module>"

# Jar directory
libDirectory = "E:\\lib"

# Module output directory
moduleDirectory = "E:\\modules"


def create_module_xml_file(main_module_path, module_name, file_name):
    module_xml = open(os.path.join(main_module_path, "module.xml"), "w")
    module_xml.write(MODULE_XML.format(module_name, file_name))
    module_xml.close()


def main():
    for fileName in os.listdir(libDirectory):
        if fileName.lower().endswith(".jar"):
            file_path = os.path.join(libDirectory, fileName)

            jar_file = zipfile.ZipFile(file_path)
            main_module_path = "";
            for info in jar_file.infolist():
                print(info.filename)
                if "-" not in info.filename and "." in info.filename:
                    module_path = info.filename[:info.filename.rfind("/")];
                    if (not main_module_path) or len(main_module_path) > len(module_path):
                        main_module_path = module_path;

            module_name = main_module_path.replace("/", ".")
            main_module_path = os.path.join(moduleDirectory, main_module_path, "main")

            # Create module path
            if not os.path.isdir(main_module_path):
                os.makedirs(main_module_path)

            # Copy jar file
            shutil.copy(file_path, main_module_path)

            # Create module.xml file
            create_module_xml_file(main_module_path, module_name, fileName)

            print(file_path.ljust(70) + " => " + main_module_path)


if __name__ == '__main__':
    main()
