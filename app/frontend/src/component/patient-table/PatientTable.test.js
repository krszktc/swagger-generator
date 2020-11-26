import React from 'react';
import { render, shallow, mount } from 'enzyme';
import PatientTable from './PatientTable';


const MOCK_COLUMNS = [
    { header: 'Header One', column_name: 'col_one', size: '20%' },
    { header: 'Header Two', column_name: 'col_two', size: '40%' },
    { header: 'Header Three', column_name: 'col_three', size: '40%' }
];

const MOCK_TABLE_DATA = {
    'data': [
        { 'attributes': { 'col_one': 'AAA_1', 'col_two': 'AAA_2', 'col_three': 'AAA_3' } },
        { 'attributes': { 'col_one': 'BBB_1', 'col_two': 'BBB_2', 'col_three': 'BBB_3' } },
        { 'attributes': { 'col_one': 'CCC_1', 'col_two': 'CCC_2', 'col_three': 'CCC_3' } }
    ]
};

const setFetchData = (data) => {
    global.fetch = jest.fn(() =>
        Promise.resolve({
            json: () => Promise.resolve(data)
        })
    );
}

describe('PatientTable component witch no data', () => {

    beforeEach(() => {
        setFetchData({});
    });

    it('renders without crashing', () => {
        shallow(<PatientTable config={MOCK_COLUMNS} />);
    });

    it('should render only-header table witchout data', () => {
        // GIVEN
        const component = render(<PatientTable config={MOCK_COLUMNS} />);
        // WHEN
        const tableHeaders = component.find('table > thead > tr th');
        // THEN
        expect(tableHeaders.length).toBe(3);
        expect(tableHeaders.get(0).firstChild.data).toBe('Header One');
        expect(tableHeaders.get(1).firstChild.data).toBe('Header Two');
        expect(tableHeaders.get(2).firstChild.data).toBe('Header Three');
    });

    it('should render table with rows in proper order', (done) => {
        // GIVEN
        setFetchData(MOCK_TABLE_DATA)
        const component = mount(<PatientTable config={MOCK_COLUMNS} />);

        setImmediate(() => {
            // WHEN
            component.update()
            const tableRows = component.find('table tbody tr');
            // THEN
            expect(tableRows.length).toBe(3);

            expect(tableRows.get(0).props.children[0].props.children).toBe('AAA_1');
            expect(tableRows.get(0).props.children[1].props.children).toBe('AAA_2');
            expect(tableRows.get(0).props.children[2].props.children).toBe('AAA_3');

            expect(tableRows.get(1).props.children[0].props.children).toBe('BBB_1');
            expect(tableRows.get(1).props.children[1].props.children).toBe('BBB_2');
            expect(tableRows.get(1).props.children[2].props.children).toBe('BBB_3');

            expect(tableRows.get(2).props.children[0].props.children).toBe('CCC_1');
            expect(tableRows.get(2).props.children[1].props.children).toBe('CCC_2');
            expect(tableRows.get(2).props.children[2].props.children).toBe('CCC_3');

            done()
        }, 0);

    });

    it('should show modal when click AddPatient', () => {
        // GIVEN 
        const component = mount(<PatientTable config={MOCK_COLUMNS} />);
        // WHEN
        component.find('button').simulate('click');
        // THEN
        expect(component.state().isModalShowed).toBe(true);
        expect(component.find('.modal-content')).toBeDefined()
    });

});