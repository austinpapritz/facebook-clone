import { useEffect, useState } from 'react';
import { getUser } from './api/user';

function App() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    getUser(1).then(setUser);
  }, []);

  return (
    <div>
      <h1>Facebook Clone</h1>
      <pre>{JSON.stringify(user, null, 2)}</pre>
    </div>
  );
}

export default App;