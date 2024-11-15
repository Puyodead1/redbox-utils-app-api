import sys

import clr

# Load the VistaDB DLL
clr.AddReference("U:/samples/VistaDB.NET20.dll")

from System import Array, Byte
from System.IO import FileAccess, FileMode, FileStream
from VistaDB import VistaDBType

# Import the VistaDB namespaces
from VistaDB.Provider import VistaDBConnection, VistaDBParameter
from VistaDB.VistaDBTypes import VistaDBBinary


class VistaHelper:
    def __init__(self, file):
        # Connection setup
        self.connection_string = f"Data Source={file}"
        self.connection = VistaDBConnection(self.connection_string)

    def get_value(self, query):
        value_string = None
        try:

            # Open the database connection
            self.connection.Open()
            command = self.connection.CreateCommand()
            command.CommandText = query

            # Execute the query and read the results
            reader = command.ExecuteReader()

            # Read each row in the result set
            while reader.Read():
                # Fetch the value of the 'Value' column and print it
                value_string = str(reader["Value"])

        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")

        finally:
            # Clean up resources
            if reader:
                reader.Close()
            if self.connection.State == "Open":
                self.connection.Close()
        return value_string

    def get_key_list(self, query):
        result = []
        try:

            # Open the database connection
            self.connection.Open()
            command = self.connection.CreateCommand()
            command.CommandText = query

            # Execute the query and read the results
            reader = command.ExecuteReader()

            # Read each row in the result set
            while reader.Read():
                # Fetch the value of the 'Value' column and print it
                result.append(str(reader["Key"]))

        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")

        finally:
            # Clean up resources
            if reader:
                reader.Close()
            if self.connection.State == "Open":
                self.connection.Close()
        return result

    def get_key_value_list(self, query):
        result = []
        try:

            # Open the database connection
            self.connection.Open()
            command = self.connection.CreateCommand()
            command.CommandText = query

            # Execute the query and read the results
            reader = command.ExecuteReader()

            # Read each row in the result set
            while reader.Read():
                # Fetch the value of the 'Value' column and print it
                result.append((str(reader["Key"]), str(reader["Value"])))

        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")

        finally:
            # Clean up resources
            if reader:
                reader.Close()
            if self.connection.State == "Open":
                self.connection.Close()
        return result

    def put_value(self, query, values: dict = {}):
        try:

            # Open the database connection
            self.connection.Open()
            command = self.connection.CreateCommand()
            command.CommandText = query

            # Clear parameters to avoid duplicate entries
            command.Parameters.Clear()

            # Create parameters based on the values dictionary
            for key, value in values.items():
                if key == "@img":
                    # Open the file and read its contents into a byte array
                    fs = FileStream(value, FileMode.Open, FileAccess.Read)
                    file_length = int(fs.Length)
                    file_data = Array[Byte](file_length)  # Create a .NET byte array of the required length
                    fs.Read(file_data, 0, file_length)  # Read the file into the byte array
                    fs.Close()  # Close the FileStream

                    # Create parameters
                    blob_param = command.CreateParameter()
                    blob_param.ParameterName = key
                    blob_param.VistaDBType = VistaDBType.Image
                    blob_param.Value = VistaDBBinary(file_data)
                else:
                    command.Parameters.AddWithValue(key, value)  # Add other parameters

            # Execute the query and read the results
            reader = command.ExecuteNonQuery()

        except Exception as e:
            # Print any errors that occur
            print(f"Error: {e}")

        finally:
            # Clean up resources
            if self.connection.State == "Open":
                self.connection.Close()
        return reader


if __name__ == "__main__":
    vista = VistaHelper("./profile.data.vdb3")
    i = vista.get_value("SELECT * FROM ProductCatalog WHERE value LIKE '{ product_id = 1002 ,%'")
    print(i)
