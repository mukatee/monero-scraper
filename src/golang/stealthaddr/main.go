package main

import (
	"encoding/hex"
	"fmt"
	"github.com/ethereum/go-ethereum/crypto"
	"go.dedis.ch/kyber/v3"
	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/util/random"
	"strconv"
)

var rng = random.New()

func main() {
	articleExample()
	//	randomExample()
}

func articleExample() {
	suite := edwards25519.NewBlakeSHA256Ed25519()
	var G kyber.Point = suite.Point().Base()
	fmt.Printf("Curve points:\n G:\t%s\n\n", G)
	var hexStr = "c595161ea20ccd8c692947c2d3ced471e9b13a18b150c881232794e8042bf107";
	value, _ := strconv.ParseInt(hexStr, 16, 64)
	fmt.Printf ("Hexadecimal '%s' is integer %d (%X)\n", hexStr, value, value)

	hexBytes, _ := hex.DecodeString(hexStr)
	//% x is hex print with space separator, %x is without separator
	fmt.Printf ("Hexadecimal '%s' is byte array % x (%X)\n", hexStr, hexBytes, hexBytes)
	r := suite.Scalar().SetBytes(hexBytes)
	byteR, _ := r.MarshalBinary()
	hash := crypto.Keccak256Hash(byteR)
	fmt.Printf ("Hexadecimal '%X' \n", hash)


}


