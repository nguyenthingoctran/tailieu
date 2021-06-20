import CartIcon from "../Cart/CartIcon";
import classes from './HeaderCardButton.module.css'

const HeaderCartButton = props => {
    return <button className={classes.button}>
        <span className={classes.icon}><CartIcon/></span>
        <span>Your Card</span>
        <span className={classes.badge}>3</span>
    </button>
}

export default HeaderCartButton;