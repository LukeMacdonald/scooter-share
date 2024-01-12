

export function CustomAuthInput({name,label, handleChange, value, className}){

    return(
        <input 
          type='text' 
          name={name}
          placeholder={`Enter ${label}`}
          className={`w-full p-2 rounded-md ${className}`}
          onChange={handleChange} 
          value={value}
        />
    )
}