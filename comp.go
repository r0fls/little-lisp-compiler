package main

import (
	"fmt"
	"strings"
	"unicode"
)

func tokenizer(code string) []map[string]string {
	current := 0
	var tokens []map[string]string
	for current < len(code) {
		char := string([]rune(code)[current])
		if char == "(" {
			token := make(map[string]string)
			token["type"] = "paren"
			token["value"] = "("
			tokens = append(tokens, token)
			current += 1
			continue
		} else if char == ")" {
			token := make(map[string]string)
			token["type"] = "paren"
			token["value"] = ")"
			tokens = append(tokens, token)
			current += 1
			continue
		} else if unicode.IsSpace([]rune(char)[0]) {
			current += 1
			continue
		} else if unicode.IsNumber([]rune(char)[0]) {
			value := []string{}
			for unicode.IsNumber([]rune(char)[0]) {
				value = append(value, char)
				current += 1
				char = string([]rune(code)[current])
			}
			token := make(map[string]string)
			token["type"] = "value"
			token["value"] = strings.Join(value, "")
			tokens = append(tokens, token)
			current += 1
			continue
		} else if unicode.IsLetter([]rune(char)[0]) {
			value := []string{}
			for unicode.IsLetter([]rune(char)[0]) {
				value = append(value, char)
				current += 1
				char = string([]rune(code)[current])
			}
			token := make(map[string]string)
			token["type"] = "value"
			token["value"] = strings.Join(value, "")
			tokens = append(tokens, token)
			current += 1
			continue
		} else {
			fmt.Println("Did not match token %s", char)
		}
	}
	return tokens
}

func parser(tokens []map[string]string) []map[string]string {
	current := 0
	func walk() {
		token := tokens[current]
		if token["type"] == "number" {
			node := make(map[string]string)
			current += 1
			node["type"] = "NumberLiteral"
			node["value"] = token["value"]
			return node
		} else if token["type"] == "paren" && token["value"] = ")" {
			current += 1
			tokens = tokens[current]
		}
	}
}

func main() {
	t := tokenizer("(add 2 (subtract 4 2))")
	for _, val := range t {
		for i, v := range val {
			fmt.Println(i, ": ", v)
		}
	}
}
