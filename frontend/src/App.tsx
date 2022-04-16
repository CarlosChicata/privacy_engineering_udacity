import './App.css';
import React from 'react';
import { H1, H4 } from "@blueprintjs/core"
import { IBallotForm } from "./BallotForm"


function App() {
  return (
    <div className="app">
      <div className="app-header">
          <H1 className="white-text"> The Republic of Atlantis </H1>
          <H4 className="white-text"> DEPARTMENT OF ELECTORAL AFFAIRS </H4>
      </div>
      <div className="form">
        <IBallotForm />
      </div>
    </div>
  );
}

export default App;
