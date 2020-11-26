import React from 'react';
import { mount, shallow } from 'enzyme';
import PatientPopup from './PatientPopup';

describe('PatientPopup component', () => {

    it('renders without crashing', () => {
        shallow(<PatientPopup show={true} />);
    });

    it('should skip sending data by incomplete form', () => {
        // GIVEN 
        let data_handled = false;
        const component = mount(<PatientPopup show={true} onHide={data => data_handled = true}/>);
        // WHEN
        component.find('form').simulate('submit', { preventDefault () {} });
        // THEN
        expect(data_handled).toBe(false);
    });

    it('should skip sending data by wrong email format', () => {
        // GIVEN 
        let data_handled = false;
        const component = mount(<PatientPopup show={true} onHide={data => data_handled = true} />);
        const submitButton = component.find('form');
        const inputList = component.find('input');
        // WHEN
        inputList.at(0).simulate('change', { target: { value: 'SomeFirstName' } });
        inputList.at(1).simulate('change', { target: { value: 'SomeLastName' } });
        inputList.at(2).simulate('change', { target: { value: 'SomeWrongEmailFormat' } });
        inputList.at(3).simulate('change', { target: { value: '1980-01-01' } });
        submitButton.simulate('submit', { preventDefault () {} });
        // THEN
        expect(data_handled).toBe(false);
    });

    it('should send data', () => {
        // GIVEN 
        let data_handled = {};
        const component = mount(<PatientPopup show={true} onHide={(data) => data_handled = data} />);
        const submitButton = component.find('form');
        const inputList = component.find('input');
        // WHEN
        inputList.at(0).simulate('change', { target: { value: 'SomeFirstName' } });
        inputList.at(1).simulate('change', { target: { value: 'SomeLastName' } });
        inputList.at(2).simulate('change', { target: { value: 'some_email@com.com' } });
        inputList.at(3).simulate('change', { target: { value: '1980-01-01' } });
        submitButton.simulate('submit', { preventDefault () {} });
        // THEN
        expect(data_handled.first_name).toBe('SomeFirstName');
        expect(data_handled.last_name).toBe('SomeLastName');
        expect(data_handled.email).toBe('some_email@com.com');
        expect(data_handled.birthdate).toBe('1980-01-01');
        expect(data_handled.sex).toBe('F');
    });

});