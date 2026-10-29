package com.example.fibonacci;

import java.util.Map;
import java.math.BigInteger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
public class Application {
  public static void main(String[] args) { SpringApplication.run(Application.class, args); }

  @RestController
  static class Controller {
    @GetMapping("/health") Map<String, String> health() { return Map.of("status", "ok"); }

    @GetMapping("/fibonacci/{n}") Map<String, Object> fibonacci(@PathVariable int n) {
      if (n < 0 || n > 100) throw new IllegalArgumentException("n must be between 0 and 100");
      BigInteger a = BigInteger.ZERO, b = BigInteger.ONE;
      for (int i = 0; i < n; i++) { BigInteger next = a.add(b); a = b; b = next; }
      return Map.of("n", n, "value", a.toString());
    }
  }
}
