import React from 'react';
import './PatientPopup.css';
import { Modal, Button, InputGroup, Form } from 'react-bootstrap';


const INIT_STATE = {
   validated: false,
   input_data: {
      first_name: '',
      last_name: '',
      email: '',
      birthdate: '',
      sex: 'F'
   }
};


class PatientPopup extends React.Component {

   constructor(props) {
      super(props);
      this.state = { ...INIT_STATE }
   }

   handleSubmit(event) {
      const form = event.currentTarget;
      if (form.checkValidity() === false) {
         event.preventDefault();
         event.stopPropagation();
         this.setState({ validated: true });
      } else {
         this.props.onHide({ ...this.state.input_data });
         this.closePopup()
      }
   }

   closePopup() {
      this.setState({ ...INIT_STATE, validated: false });
   }

   render() {
      return (
         <Modal {...this.props}
            size="lg"
            animation={false}
            aria-labelledby="contained-modal-title-vcenter"
            centered>
            <Modal.Header closeButton onClick={() => this.closePopup()}>
               <Modal.Title id="contained-modal-title-vcenter">
                  Add Patient
               </Modal.Title>
            </Modal.Header>
            <Form noValidate
               validated={this.state.validated}
               onSubmit={event => this.handleSubmit(event)}>
               <Modal.Body>

                  <Form.Group md="4">
                     <InputGroup>
                        <InputGroup.Prepend>
                           <InputGroup.Text>First Name</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Form.Control type="text" required
                           value={this.state.input_data.first_name}
                           onChange={event => this.setState({ input_data: { ...this.state.input_data, first_name: event.target.value } })} />
                     </InputGroup>
                  </Form.Group>

                  <Form.Group md="4">
                     <InputGroup>
                        <InputGroup.Prepend>
                           <InputGroup.Text>Last Name</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Form.Control type="text" required
                           value={this.state.input_data.last_name}
                           onChange={event => this.setState({ input_data: { ...this.state.input_data, last_name: event.target.value } })} />
                     </InputGroup>
                  </Form.Group>

                  <Form.Group md="4">
                     <InputGroup>
                        <InputGroup.Prepend>
                           <InputGroup.Text>E-mail</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Form.Control type="email" required
                           value={this.state.input_data.email}
                           onChange={event => this.setState({ input_data: { ...this.state.input_data, email: event.target.value } })} />
                     </InputGroup>
                  </Form.Group>

                  <Form.Group md="4">
                     <InputGroup>
                        <InputGroup.Prepend>
                           <InputGroup.Text>Birth Date</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Form.Control type="date" required
                           value={this.state.input_data.birthdate}
                           onChange={event => this.setState({ input_data: { ...this.state.input_data, birthdate: event.target.value } })} />
                     </InputGroup>
                  </Form.Group>

                  <Form.Group md="4">
                     <InputGroup>
                        <InputGroup.Prepend>
                           <InputGroup.Text>Sex</InputGroup.Text>
                        </InputGroup.Prepend>
                        <Form.Control as="select"
                           value={this.state.input_data.sex}
                           onChange={event => this.setState({ input_data: { ...this.state.input_data, sex: event.target.value } })} required>
                           <option value="M">M</option>
                           <option value="F">F</option>
                        </Form.Control>
                     </InputGroup>
                  </Form.Group>

               </Modal.Body>
               <Modal.Footer>
                  <Button type="submit">Save</Button>
               </Modal.Footer>
            </Form>
         </Modal>
      );
   }
}

export default PatientPopup;


