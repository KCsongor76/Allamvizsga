import React from "react";
import classes from "./LabelInput.module.css";

const LabelInput = ({
  labelText,
  type,
  id,
  name,
  value,
  setter,
  placeholder,
}) => {
  return (
    <label className={classes.label}>
      {labelText}
      <input
        className={classes.input}
        type={type}
        id={id}
        name={name}
        value={value}
        placeholder={placeholder}
        onChange={(event) => setter(event.target.value)}
      />
    </label>
  );
};

export default LabelInput;
