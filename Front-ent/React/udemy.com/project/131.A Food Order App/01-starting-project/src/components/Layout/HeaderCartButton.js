import CartIcon from "../Cart/CartIcon";
import classes from './HeaderCardButton.module.css';
import CartContext from '../../store/cart-context';
import { useContext, useEffect, useState } from 'react';

const HeaderCartButton = props => {
    const [btnIsHighlighted, setBtnIsHighlighted] = useState(false);
    const cartCtx = useContext(CartContext);
    const { items } = cartCtx;

    const numberOfCartitems = cartCtx.items.reduce((curNumber, item) => {
        console.log(item, "item")
        return curNumber + item.amount;
    }, 0);
    
    const btnClasses = `${classes.button} ${btnIsHighlighted ? classes.bump : ''}`;


    useEffect(() => {
        if (items.length === 0){
            return;
        }
        setBtnIsHighlighted(true);

        const timer = setTimeout(() => {
            setBtnIsHighlighted(false);
        }, 300);

        return () => {
            clearTimeout(timer)
        }

    }, [items]);

    return <button className={btnClasses} onClick={props.onClick}>
        <span className={classes.icon}><CartIcon/></span>
        <span>Your Card</span>
        <span className={classes.badge}>{numberOfCartitems}</span>
    </button>
}

export default HeaderCartButton;