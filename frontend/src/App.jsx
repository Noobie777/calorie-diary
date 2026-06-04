import { useState } from "react";
import './App.css'
import FoodLog from "./FoodLog";

function App(){
  const [foodName, setFoodName] = useState("");
  const [logs, setLogs] = useState([
    {
      id: 1,
      food_name: 'Chicken Breast',
      calories: 300
    },
    {
      id: 2,
      food_name: "Rice",
      calories: 200
    },
    {
      id: 3,
      food_name: "Protein Shake",
      calories: 180
    }
  ])
  function addFood(){
    if (foodName.trim() === ""){
    return;
  }
    setLogs([
      ...logs,
      {
        id: logs.length + 1,
        food_name: foodName.trim(),
        calories: 150
      }
    ]);
    setFoodName("");
  }
  function deleteFood(id){
    setLogs(
      logs.filter((log) => log.id !== id)
    );
  }
  return(
    <div>
      <h1>Calorie Diary</h1>
      <p>Current Food: {foodName}</p>
      <input 
        value={foodName}
        onChange={(event) =>{
          setFoodName(event.target.value);
      }}/>
      <button onClick={addFood}>Add Food</button>

      {logs.map((log) => (
        <FoodLog
          key={log.id}
          id={log.id}
          food_name={log.food_name}
          calories={log.calories}
          deleteFood={deleteFood}
        />
      ))}
      </div>
  )
}

export default App