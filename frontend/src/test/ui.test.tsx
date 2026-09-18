import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { Button } from "../components/ui/Button";
import LoginPage from "../pages/LoginPage";
import { AuthProvider } from "../context/AuthContext";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

describe("Button", () => {
  it("renders label", () => {
    render(<Button>Analyze</Button>);
    expect(screen.getByText("Analyze")).toBeInTheDocument();
  });
});

describe("Login form", () => {
  it("shows validation-ready fields", () => {
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <AuthProvider>
          <MemoryRouter>
            <LoginPage />
          </MemoryRouter>
        </AuthProvider>
      </QueryClientProvider>,
    );
    expect(screen.getByText("Sign in")).toBeInTheDocument();
    expect(screen.getByText("Email")).toBeInTheDocument();
  });
});
