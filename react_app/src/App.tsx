import React from 'react';
import logo from './logo.svg';
import './App.css';
import 'typeface-roboto';
import {FormControl, InputLabel} from '@material-ui/core'

import {ConfigPage} from './components/ConfigPage'

const App: React.FC = () => {
  return (
    <div className="container">
      <ConfigPage/>

    </div>
  );
}

export default App;
