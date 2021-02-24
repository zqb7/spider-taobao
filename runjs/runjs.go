package main

import "C"

import (
	"fmt"

	"github.com/robertkrimen/otto"
)

var vm *otto.Otto

func init() {
	vm = otto.New()
}

//export runjs
func runjs(js *C.char) *C.char {
	value, err := vm.Run(C.GoString(js))
	if err != nil {
		return C.CString(fmt.Sprintf("%v", err))
	}
	return C.CString(fmt.Sprintf("%v", value))
}

func main() {
}
