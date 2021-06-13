import React, {useState, useRef} from 'react';

import Card from '../UI/Card';
import Button from '../UI/Button';
import ErrorModal from '../UI/ErrorModal';
import Wrapper from '../Helpers/Wrapper';
import classes from './AddUser.module.css';

const AddUser = props => {
    const nameInputRef = useRef();
    const ageInputRef = useRef();

    const [enteredUsername, setEnterUsername] = useState('');
    const [enteredAge, setEnteredAge] = useState('');
    const [error, setError] = useState();

    const addUserHandler = (event) => {
        event.preventDefault();
        const enteredName = nameInputRef.current.value;
        const enteredAge = ageInputRef.current.value;
        if (enteredUsername.trim().length === 0 || enteredAge.trim().length ===0){
            setError({
                title: 'Invalid input',
                message: 'Please enter a valid name and age (non-empty values)'
            });
        }
        if (+enteredAge < 1){
            setError({
                title: 'Invalid age',
                message: 'Please enter a valid age (> 0)'
            });
        }
        props.onAddUser(enteredUsername, enteredAge)
        setEnterUsername('');
        setEnteredAge('');
    }

    const usenameChangeHandler = (event) => {
        setEnterUsername(event.target.value);
    };

    const ageChangeHandler = (event) => {
        setEnteredAge(event.target.value);
    };

    const errorHandler = () => {
        setError(null);
    };

    return (
        <Wrapper>
            {error && 
                <ErrorModal 
                    title={error.title} 
                    message={error.message}
                    onConfirm={errorHandler}/>}
            <Card className={classes.input} >
                <form onSubmit={addUserHandler}>
                    <label htmlFor="username">Username</label>
                    <input id="username" 
                            type="text" 
                            value={enteredUsername}
                            onChange={usenameChangeHandler} 
                            ref={nameInputRef}/>
                    <label htmlFor="age">Age (Years)</label>
                    <input id="age" 
                            type="number" 
                            value={enteredAge}
                            onChange={ageChangeHandler}
                            ref={ageInputRef}/>
                    <Button type="submit">Add User</Button>
                </form>    
            </Card>
        </Wrapper>
    );
};

export default AddUser;