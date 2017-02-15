import os
import argparse
import json
import shutil
from mako.template import Template

class Main:
    structure_file = ""
    module_name = ""
    structure_data = ""
    workspace_dir = ""
    current_dir = ""
    packages = {}
    
    def make_clean_workspace(self):
        print( "Creating Workspace Directory" )
        if os.path.isdir('workspace'):
            print( "Workspace Directory exists, deleting" )
            shutil.rmtree('workspace')
        os.mkdir('workspace')
        print( "Workspace Directory Created" )
        print( "" )

    def generate_from_template(self, template):
        fn = "templates/{0}".format( template )
        print( "Using template: {0}".format( fn ) )
        mytemplate = Template( filename=fn )
        return mytemplate.render(module_name=self.module_name, install_version="${install_version}", packages=self.packages)
    
    def create_files(self, data, directory):
        for item in data:
            if item["type"] == "file":
                print( "Current Directory: {0}".format( directory ) )
                print( "File: {0}".format( item["path"] ) )
                if 'template' in item.keys():
                    print( "template: {0}".format( item["template"] ) )
                    output = self.generate_from_template( item["template"] )
                    out_file = open( os.path.join( directory, item["name"] ), 'w' )
                    out_file.write( output )
                    out_file.close()
                    print( "Created file: {0}".format( item["name"] ) )
                else:
                    shutil.copyfile( 'templates/' + item["name"], os.path.join( directory, item["name"] ) )
            else:
                print( "Folder: {0}".format( item["name"] ) )
                self.current_dir = os.path.join( directory, item["name"] )
                print( "Creating subfolder: {0}".format( self.current_dir ) )
                os.mkdir( self.current_dir )
                self.create_files( item["children"], self.current_dir )

    def parse_structure(self):
        print( "Parsing Module Structure" )
        with open(self.structure_file) as json_file:
            self.structure_data = json.load(json_file)

    def parse_resources(self):
        for resource in self.structure_data["resources"]:
            if resource["type"] == "package":
                package = {}
                package[ resource["name"] ] = resource["ensure"]
                self.packages.update(package)
                print( "Adding package resource {0} at version {1}".format( resource["name"], resource["ensure"] ) )

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--name', required=True, help='Module Name')
        parser.add_argument('-s', '--structure', required=True, help='json structure file')
        args = parser.parse_args()
        self.structure_file = args.structure
        self.module_name = args.name

        # create clean workspace
        self.make_clean_workspace()

        # parse the desired structure of the puppet module
        self.parse_structure()
        self.parse_resources()
        
        # change to the workspace
        cwd = os.getcwd()
        self.workspace_dir = os.path.join( cwd, "workspace" )
        self.current_dir = self.workspace_dir
        print( "current workspace: {0}".format( self.workspace_dir ) )


        # create the file and folder structure
        file_data =  self.structure_data["structure"]
        self.create_files( file_data, self.workspace_dir )

if __name__ == '__main__':
    mymain = Main()
    mymain.main()

