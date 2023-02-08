import { Welcome } from '../components/Welcome/Welcome';
import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import Login from '../components/Login';

export default function HomePage() {
  return (
    <>
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}
      >
        <Login />
      </div>
      <div style={{ position: 'fixed', bottom: '2vh', right: '2vw' }}>
        <ColorSchemeToggle />
      </div>
      <Welcome />

      {/* <Googlemapscomponent /> */}
    </>
  );
}
