import './ResultFilterItem.css'

const ResultFilterItem = (props) => {
  console.log(props)
  return (
    <div className="result-filter-item">
      <div className="result-column"></div>
      <span className="result-month">{props.month}</span>  
    </div>
  )
}

export default ResultFilterItem