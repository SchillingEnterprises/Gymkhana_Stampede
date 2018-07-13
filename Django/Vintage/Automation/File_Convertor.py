import csv
import json
import os

import dropbox
from xmlutils.xml2csv import xml2csv
from xmlutils.xml2json import xml2json
from xmlutils.xml2sql import xml2sql


class DropBox:
    @staticmethod
    def input_file():
        # Get your app key and secret from the Dropbox developer website
        app_key = input('INSERT_APP_KEY')
        app_secret = input('INSERT_APP_SECRET')

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print('1. Go to: ' + authorize_url)
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = input(r"Enter the authorization code here: ").strip()

        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)

        client = dropbox.client.DropboxClient(access_token)
        print('linked account: ', client.account_info())

        f = open('working-draft.txt', 'rb')
        response = client.put_file('/magnum-opus.txt', f)
        print('uploaded: ', response)

        folder_metadata = client.metadata('/')
        print('metadata: ', folder_metadata)

        f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
        out = open('magnum-opus.txt', 'wb')
        out.write(f.read())
        out.close()
        print(metadata)


class FileConverter:
    @property
    def csv2json(self, base_filename=None):
        """
        :rtype: JSON
        """
        with open(self.file_name(suffix='.csv'), 'r') as file:
            reader = csv.reader(file, delimiter=';')
            data_list = list()
            for row in reader:
                data_list.append(row)
        csv_data_being_converted = [dict(zip(data_list[0], row)) for row in data_list]
        csv_data_being_converted.pop(0)
        converted_data_to_json = json.dumps(csv_data_being_converted)
        base_filename.json = converted_data_to_json
        return self.file_name(suffix='.json')

    @property
    def dat2json(self, base_filename=None):
        """
        :rtype: JSON
        """
        header = [input("Header Fields")]

        with open(self.file_name(suffix='.DAT')) as datfile:
            with open('output.csv', 'wb') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                for line in datfile:
                    base_filename.json = writer.writerow(json.loads(line))
                return self.file_name(suffix='.json')

    @property
    def string_file2string_json_file(self):
        """
        :rtype: TXT JSON String
        """
        with open(self.file_name(suffix='.txt'), "rb") as file_in:
            content = json.load(file_in)
        with open(self.file_name(suffix='.txt'), "wb") as file_out:
            json.dump(content, file_out, indent=1)
        return self.file_name(suffix='.txt')

    @property
    def txt2json(self):
        with open(self.file_name(suffix='.txt'), 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ')
            i = 0
            header = []
            out_data = []
            for row in filereader:
                row = [elem for elem in row if elem]
                if i == 0:
                    i += 1
                    header = row
                else:
                    row[0:2] = [row[0] + " " + row[1]]
                    _dict = {}
                    for elem, header_elem in zip(row, header):
                        _dict[header_elem] = elem
                    out_data.append(_dict)
        return self.file_name(suffix='.json') == print(json.dumps(out_data))

    @property
    def xml2csv(self):
        """
        :rtype: CSV
        """
        converter = xml2csv(self.file_name(suffix='.xml'), self.file_name(suffix='.csv'), encoding="utf-8")
        converter.convert(tag="item")
        return self.file_name(suffix='.csv')

    @property
    def xml2json(self):
        """
        :rtype: JSON
        """
        converter = xml2json(self.file_name(suffix='.xml'), self.file_name(suffix='.json'), encoding="utf-8")
        converter.convert()
        return self.file_name(suffix='.json')

    @property
    def xml2sql(self):
        """
        :rtype: SQL
        """
        converter = xml2sql(self.file_name(suffix='.xml'), self.file_name(suffix='.sql'), encoding="utf-8")
        converter.convert(tag="item", table="table")
        return self.file_name(suffix='.sql')

    def file_name(self, suffix=None):
        directory_path = input("Directory Path: ")
        base_filename = input("Base Filename: ")
        if suffix is not None:
            os.path.join(directory_path, "{0}{1}".format(base_filename, suffix))
        else:
            raise NotImplementedError
