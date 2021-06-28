import CartIcon from "../Cart/CartIcon";
import classes from './HeaderCardButton.module.css';
import CartContext from '../../store/cart-context';
import { useContext } from 'react';

const HeaderCartButton = props => {
    const cartCtx = useContext(CartContext);

    console.log(cartCtx.items,"cartCtx")

    const numberOfCartitems = cartCtx.items.reduce((curNumber, item) => {
        console.log(item, "item")
        return curNumber + item.amount;
    }, 0);

    return <button className={classes.button} onClick={props.onClick}>
        <span className={classes.icon}><CartIcon/></span>
        <span>Your Card</span>
        <span className={classes.badge}>{numberOfCartitems}</span>
    </button>
}

export default HeaderCartButton;