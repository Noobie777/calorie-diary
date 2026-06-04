function FoodLog(props){
    return (
        <div className="food-log">
        <p>{props.food_name} has {props.calories} calories</p>
        <button onClick = {() => props.deleteFood(props.id)}>Delete Food</button>
        </div>
    )
}

export default FoodLog