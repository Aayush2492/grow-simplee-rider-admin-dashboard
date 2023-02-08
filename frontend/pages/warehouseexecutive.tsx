import { useToggle, upperFirst } from '@mantine/hooks';
import { useForm } from '@mantine/form';
import { TextInput, PasswordInput, Button, Text, Paper, PaperProps } from '@mantine/core';
import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { FileInput } from '@mantine/core';
import { IconUpload } from '@tabler/icons';
import { useState } from 'react';

function Warehouseexecutive(props: PaperProps) {
  const [weight, setweight] = useState(0.0);
  const [file, setfile] = useState<File | null>(null);
  const submithandler = () => {};
  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', justifyContent: 'center' }}>
      <Paper
        radius="md"
        style={{
          maxWidth: 400,
          maxHeight: 700,
          margin: 'auto',
        }}
        p="xl"
        {...props}
      >
        <Text style={{ fontSize: 24, fontWeight: 'bolder' }}>Warehouse Executive Section</Text>
        <FileInput
          label="Upload image of item"
          placeholder="Upload image of item"
          icon={<IconUpload size={14} />}
          style={{ margin: 20 }}
          value={file}
          onChange={(e) => setfile(e)}
          accept="image/png,image/jpeg"
        />
        <TextInput
          label="Dead weight of item"
          style={{ margin: 20 }}
          value={weight}
          onChange={(e) => setweight(parseFloat(e.target.value))}
        />
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <Button type="button" onClick={() => submithandler()}>
            Compute Volumetric Weight
          </Button>
        </div>
        <div style={{ position: 'fixed', bottom: '2vh', right: '2vw' }}>
          <ColorSchemeToggle />
        </div>
      </Paper>
    </div>
  );
}

export default Warehouseexecutive;
