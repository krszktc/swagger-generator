import React from 'react';
import './PatientTable.css';
import { Card, Table, Button } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import PatientPopup from '../patient-popup/PatientPopup';


const requestHeaders = { 'Content-Type': 'application/json' };

class PatientTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            tableData: [],
            isModalShowed: false
        };
    }

    componentDidMount() {
        this.getPatientsData();
    }

    getPatientsData() {
        fetch('/v1/patients', requestHeaders)
            .then(response => response.json())
            .then(data => {
                if (data && data.data) {
                    const newState = data.data.map(patient => patient.attributes);
                    this.setState({ tableData: [...newState] });
                }
            })
            .catch(err => console.error(err));
    }

    savePatient(requestBody) {
        const requestOptions = {
            method: 'POST',
            headers: requestHeaders,
            body: requestBody
        };
        fetch('/v1/patients', requestOptions)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    toast.error(data.error.detail)
                } else {
                    toast.success('Patient saved');
                    this.getPatientsData()
                }
            })
            .catch(err => console.error(err));
    }

    showModal() {
        this.setState({ isModalShowed: true });
    }

    hideModal(formData) {
        if (formData) {
            this.savePatient(JSON.stringify({ data: formData }));
        }
        this.setState({ isModalShowed: false });
    }

    render() {
        const headers = this.props.config.map((column, rowId) => (
            <th style={{ width: column.size }} key={rowId}>
                {column.header}
            </th>
        ));
        const rows = this.state.tableData.map((row, rowId) => {
            const cel_row = this.props.config.map((column, columnId) => (
                <td style={{ width: column.size }} key={columnId}>
                    {row[column.column_name]}
                </td>
            ));
            return (
                <tr key={rowId}>
                    {cel_row}
                </tr>
            );
        });
        return (
            <Card>
                <Card.Body>
                    <div className="table-header-container">
                        <Table bordered>
                            <thead>
                                <tr>
                                    {headers}
                                </tr>
                            </thead>
                        </Table>
                    </div>
                    <div className="table-body-container">
                        <Table hover striped bordered>
                            <tbody>
                                {rows}
                            </tbody>
                        </Table>
                    </div>
                </Card.Body>
                <Card.Body>
                    <Button variant="primary" onClick={() => this.showModal()}>Add Patient</Button>
                    <PatientPopup show={this.state.isModalShowed} onHide={formData => this.hideModal(formData)} />
                    <ToastContainer position="top-right" autoClose={5000} />
                </Card.Body>
            </Card>
        );
    }
}

export default PatientTable;