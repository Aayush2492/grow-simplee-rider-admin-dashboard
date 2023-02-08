import React, { useContext, useState } from 'react';
import { Textarea } from '@mantine/core';
import { Button } from '@mantine/core';
import { PositionContext } from '../../context';
import { FileInput } from '@mantine/core';
import { IconUpload } from '@tabler/icons';
import readXlsxFile from 'read-excel-file';

function AddressDrawer() {
  const [add, setadd] = React.useState('');
  const [rows, setrows] = useState([]);
  const [csvfile, setcsvfile] = useState<File | null>(null);
  const { BASE_URL } = useContext(PositionContext);
  async function addaddress(addressname: string) {
    let another;
    try {
      another = await fetch(`${BASE_URL}/addaddress/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          address: addressname,
        }),
      });

      if (!another.ok) {
        // throw new Error('Error in fetch addaddress/');
      }
    } catch (err) {
      // alert('error caught in fetch addaddress/');
      console.log(err);
      return;
    }
  }
  async function addaddresscsv() {
    if (csvfile) {
      readXlsxFile(csvfile).then((rows) => {
        // `rows` is an array of rows
        // each row being an array of cells.
        rows.forEach((element, index) => {
          if (element[0] != 'address') {
            addaddress(element[0].toString());
            console.log(index, element[0].toString());
          }
        });
      });
      console.log(rows);
    }
  }
  return (
    <div>
      <Textarea
        placeholder="Add Address eg : 21, 24th Main Road, 6th Phase, JP Nagar, Bangalore"
        label="Add address"
        withAsterisk
        value={add}
        onChange={(e) => setadd(e.target.value)}
      />
      <br />
      <Button variant="filled" onClick={() => addaddress(add)}>
        Add Address into DB
      </Button>
      <br />
      <br />
      <FileInput
        label="Upload csv file containing address column"
        icon={<IconUpload size={14} />}
        value={csvfile}
        onChange={(e) => setcsvfile(e)}
        accept="csv"
      />
      <br />
      <Button variant="filled" onClick={() => addaddresscsv()}>
        Add Address via csv file
      </Button>
    </div>
  );
}

export default AddressDrawer;
