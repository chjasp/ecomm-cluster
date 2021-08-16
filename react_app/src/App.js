import styled from "styled-components";
import NavbarBS from "./components/NavbarBS";
import Products from "./components/Products";
import ProductPage from "./components/ProductPage";

import { BrowserRouter as Router, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <StyledNavbarBS />
      <Route path="/" exact component={Products} />
      <Route path='/product/:id' component={ProductPage} />
    </Router>
  );
}

export default App;

const StyledNavbarBS = styled(NavbarBS)`
`;