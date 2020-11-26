import React from 'react';
import { COLUMN_ORDER } from './component/patient-table/TableConfig';
import PatientTable from './component/patient-table/PatientTable';
import './App.css';

function App() {
  return (
   <PatientTable config={COLUMN_ORDER}/>
  );
}

export default App;
