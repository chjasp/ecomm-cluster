import React, { Component, useState, useEffect, useRef } from "react";
import styled from "styled-components";
import DBObject from "./DBObject.js";
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import AllProducts from "../AllProducts";
import "./Product.css";
import axios from "axios";
import {
  Row,
  Col,
  Image,
  ListGroup,
  Button,
  Card,
  Form,
} from "react-bootstrap";

const wstyles = {
  height: "100%",
  width: "100%",
  position: "relative",
};

const cstyles = {
  height: "100%",
  width: "100%",
  position: "relative",
};

const Products = () => {
  const [price, setPrice] = useState(false);
  const [priceBool, setPriceBool] = useState(false);
  const [cw, setCw] = useState("");
  const [cwBool, setCwBool] = useState(false);
  const [input, setInput] = useState("");
  const [refresh, setRefresh] = useState(true);
  const [prodIdxs, setProdIdxs] = useState([]);
  const [prodCols, setProdCols] = useState([]);

  const [selectedFile, setSelectedFile] = useState(null);

  const intervals = [10, 20, 30, 40, 50, 60, 80, 100, 120, 1000];
  const colorScale = [
    "#640926",
    "#7B0D48",
    "#921271",
    "#A817A2",
    "#A21DBD",
    "#9539C8",
    "#8F55D3",
    "#8F73DC",
    "#9891E5",
    "#AFB5ED",
  ];

  var customBtn = null;
  var realFileBtn = null;
  var customTxt = null;
  useEffect(() => {
    handleFilter();
    console.log("------IN------");
  }, []);

  function borderAssignment(price) {
    for (let i = 0; i < intervals.length; i++) {
      if (intervals[i] > price) {
        return colorScale[i];
      }
    }
    return "#640926";
  }

  async function crazyFilter() {
    const data = await handleFilter("crazy");
    console.log(data);
    console.log("CRAZYFILTERLOG");
    console.log(prodIdxs);
    setRefresh(!refresh);
  }

  function priceFilter() {
    const colors = AllProducts.map((el) => borderAssignment(el.price));
    console.log(colors);
    setProdCols(colors);
  }

  async function handleFilter(mode_var = "default") {
    let formData = new FormData();
    formData.append("mode", mode_var);
    let out = await callBackend(formData);

    console.log(out);
    setProdIdxs(out);
    return out;
  }

  async function callBackend(data) {
    return fetch("http://localhost:8000/api/img_filter/", {
      method: "POST",
      body: data,
      mode: "cors",
    })
      .then((response) => {
        return response.json();
      })
      .then((response) => {
        return response.result;
      });
  }

  function handleInput(event) {
    event.preventDefault();
    if (input == "crazy") {
      setCw(input);
      setCwBool(!cwBool);
      crazyFilter();
      console.log("CF-----");
    } else {
      setPriceBool(true);
      priceFilter();
      console.log(input);
    }
  }

  async function fileUploadHandler() {
    let out = await uploader();
    setProdIdxs(out);
    console.log("WHAT IS OUT??");
    console.log(out[4]);
    console.log(out);
  }

  async function uploader() {
    const data = new FormData();
    data.append("file", selectedFile);

    return fetch("http://localhost:8000/api/img_similarity/", {
      method: "POST",
      body: data,
      mode: "cors",
    })
      .then((response) => {
        return response.json();
      })
      .then((response) => {
        return response.result;
      });
  }

  const fileSelectHandler = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const reset = () => {
    var new_cols = prodCols.map((item) => "transparent"); 
    setProdCols(new_cols);
    handleFilter();
    setCwBool(false);
    setPriceBool(false);
  };

  return (
    <Container class="container">
      <Map>
        <Col md={12}>
          <ListGroup variant="flush">
            <Settings>
              <h5>Settings: </h5>{" "}
              <StyledForm className="rounded-left">
                <StyledControl
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="What are you looking for?"
                />
                <Button
                  variant="primary"
                  type="submit"
                  onClick={(e) => handleInput(e)}
                >
                  Submit
                </Button>
              </StyledForm>
              <FileWrapper>
                <input type="file" onChange={fileSelectHandler} />
                <button onClick={fileUploadHandler}>Upload</button>
              </FileWrapper>
              <ResetButton
                  variant="primary"
                  type="submit"
                  onClick={reset}
                >Reset</ResetButton>
            </Settings>

            <Settings>
              {priceBool ? (
                <Scale>
                  <span id="s1">10€ </span>
                  <span id="s2">- 150€</span>
                </Scale>
              ) : (
                <div style={{ color: "white" }}>dd</div>
              )}
              {cwBool ? (
                <CWrapper>{cw}</CWrapper>
              ) : (
                <div style={{ color: "white" }}>dd</div>
              )}
            </Settings>
          </ListGroup>
        </Col>
        <TransformWrapper className="wrapper">
          <TransformComponent
            className="component"
            wrapperStyle={wstyles}
            contentStyle={cstyles}
          >
            {Object.entries(prodIdxs).map((item) => (
              <DBObject
                imgIdx={item[0]}
                x={item[1][0]}
                y={item[1][1]}
                color={prodCols[item[0]]}
              />
            ))}
          </TransformComponent>
        </TransformWrapper>
      </Map>
    </Container>
  );
};

export default Products;

const ResetButton = styled.button`
  border-radius: 3rem;
  background: #ef2779;
  border: none;
  color: white;
  height: 3rem;
  margin-left: 2rem;

  &:hover {
    background-color: #ef2779;
    color: white;
    box-shadow: 0px 13px 16px -13px black;
  }

  &:focus {
    background-color: #ef2779;
    color: white;
    box-shadow: 0px 13px 16px -13px black;
  }
`;

const FileWrapper = styled.div`
  display: flex;
  justify-content: left;
  align-items: center;
  flex-direction: column;
  padding: 0.5rem;
  border-radius: 1rem;
  width: 17rem;

  margin-left: -12rem;

  border: 3px solid #ef2779;

  input {
    height: 1.7rem;
    margin-left: 3rem;

    button {
      border-radius: 8rem;
    }

  }

  button {
    height: 1.7rem;
    margin-right: 11rem;
  }
`;

const CWrapper = styled.div`
  margin-left: 2rem;
  padding-left: 1rem;
  padding-right: 1rem;
  border-radius: 0.4rem;
  border: 3px solid #ef2779;
`;

const StyledControl = styled(Form.Control)`
  width: 15rem;
  border-radius: 1rem !important;
  margin-right: 2rem;
`;

const Settings = styled(ListGroup.Item)`
  display: flex;
  justify-content: left;
  align-items: center;
  flex-direction: row;
`;

const StyledForm = styled(Form)`
  width: 30%;
  margin-top: -0.6rem;
  // max-width: 300px;
  margin-left: 2rem;
  display: flex;
  justify-content: left;
  align-items: center;
  flex-direction: row;

  &.fc {
    height: 10%;
  }

  Button {
    border-radius:1rem;
    background: #ef2779;

    &:hover {
      background-color: #ef2779;
      color: white;
      box-shadow: 0px 13px 16px -13px black;
    }

    &:focus {
      background-color: #ef2779;
      color: white;
      box-shadow: 0px 13px 16px -13px black;
    }
  }

  border-radius: 5rem !important;
`;

const Scale = styled.div`
  width: 15%;
  max-width: 100px;
  border: 3px solid #ef2779;
  color: white;
  border-radius: 0.4rem;
  text-align: center;
  background: linear-gradient(to right, #640926 0%, #a21dbd 51%, #afb5ed 100%);
`;

const Map = styled.div`
  width: 100%;
  height: 100%;
  margin-top: 6rem;
  // border: 3px solid black;
  overflow: auto;
  cursor: pointer;
`;

const Container = styled.div`
  width: 100%;
  height: 100vh;
  margin-bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;
