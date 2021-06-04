import './Filter.css'
import ResultFilterItem from './ResultFilterItem'

const Filter = () => {

  const data_month = [{
    '2019' : {
                'Jan': 10,
                'Feb': 20,
                'Mar': 30,
                'Apr': 40,
                'May': 50,
                'Jun': 60,
                'Jul': 70,
                'Aug': 80,
                'Sep': 90,
                'Oct': 100,
                'Nov': 110,
                'Dec': 120
              },
    '2020' : {
                'Jan': 20,
                'Feb': 30,
                'Mar': 40,
                'Apr': 50,
                'May': 60,
                'Jun': 70,
                'Jul': 80,
                'Aug': 90,
                'Sep': 100,
                'Oct': 110,
                'Nov': 120,
                'Dec': 130
              },
    '2021' : {
                'Jan': 30,
                'Feb': 40,
                'Mar': 50,
                'Apr': 60,
                'May': 70,
                'Jun': 80,
                'Jul': 90,
                'Aug': 100,
                'Sep': 110,
                'Oct': 120,
                'Nov': 130,
                'Dec': 140
              },
  '2022' : {
                'Jan': 40,
                'Feb': 50,
                'Mar': 60,
                'Apr': 70,
                'May': 80,
                'Jun': 90,
                'Jul': 100,
                'Aug': 110,
                'Sep': 120,
                'Oct': 130,
                'Nov': 140,
                'Dec': 150
              }
  }

  ];

  let data_month_value = data_month.map((item) => {
    return item
  });

  console.log(data_month_value)

  return (
    <div>
      <div className="filter-select">
        <label className="label">Filter by year</label>
        <select name="filter" id="filter">
          <option value="2019">2019</option>
          <option value="2020">2020</option>
          <option value="2021">2021</option>
          <option value="2022">2022</option>
        </select>
      </div>

      <div className="result-filter">
        
        <ResultFilterItem month="Jan"/>
        <ResultFilterItem month="Feb"/>
        <ResultFilterItem month="Mar"/>
        <ResultFilterItem month="Apr"/>
        <ResultFilterItem month="May"/>
        <ResultFilterItem month="Jun"/>
        <ResultFilterItem month="Jul"/>
        <ResultFilterItem month="Aug"/>
        <ResultFilterItem month="Sep"/>
        <ResultFilterItem month="Oct"/>
        <ResultFilterItem month="Nov"/>
        <ResultFilterItem month="Dec"/>
      </div>
    </div>
  )
}

export default Filter