package main

import (
	"strconv"

	"encoding/hex"
	"fmt"
	"go.dedis.ch/kyber/v3"
	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/sign/anon"
	"os"
)

func main() {
	m:="Hello"
	scope :="My Link"
	n:=4

	argCount := len(os.Args[1:])

	if (argCount>0) {m= string(os.Args[1])}
	if (argCount>1) {n,_= strconv.Atoi(os.Args[2])}
	if (argCount>2) {scope= string(os.Args[3])}

	S := []byte(scope) // scope for linkage tags

	M := []byte(m)

	suite :=  edwards25519.NewBlakeSHA256Ed25519()

	rand := suite.RandomStream()

	// Create an anonymity set of random "public keys"
	X := make([]kyber.Point, n)
	for i := range X { // pick random points
		X[i] = suite.Point().Pick(rand)
	}

	fmt.Printf("Message: %s\nLinkable address: %s\n\n",M,S)
	fmt.Printf("Public keys: %s\n\n",X)

	// Make two actual public/private keypairs (X[mine],x)
	mine1 := 1 // only the signer knows this
	mine2 := 2

	x1 := suite.Scalar().Pick(rand) // create a private key x
	x2 := suite.Scalar().Pick(rand)

	X[mine1] = suite.Point().Mul(x1, nil) // corresponding public key X
	X[mine2] = suite.Point().Mul(x2, nil)

	fmt.Printf("Private key of signer: %s\n\n",x1)
	fmt.Printf("Public key of signer: %s\n\n",X[1])

	// Generate two signatures using x1 and two using x2
	var sig [4][]byte

	sig[0] = anon.Sign(suite, M, anon.Set(X), S, mine1, x1)
	sig[1] = anon.Sign(suite, M, anon.Set(X), S, mine1, x1)
	sig[2] = anon.Sign(suite, M, anon.Set(X), S, mine2, x2)
	sig[3] = anon.Sign(suite, M, anon.Set(X), S, mine2, x2)
	for i := range sig {
		fmt.Printf("Signature %d:\n%s", i, hex.Dump(sig[i]))
	}

	// Verify the signatures against the correct message
	var tag [4][]byte
	for i := range sig {
		goodtag, err := anon.Verify(suite, M, anon.Set(X), S, sig[i])
		if err != nil {
			panic(err.Error())
		}
		tag[i] = goodtag
		if tag[i] == nil || len(tag[i]) != suite.PointLen() {
			panic("Verify returned invalid tag")
		}
		fmt.Printf("Sig%d tag: %s\n", i,
			hex.EncodeToString(tag[i]))
	}

}