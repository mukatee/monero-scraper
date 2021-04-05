package main

import (
	"fmt"
	"go.dedis.ch/kyber/v3"
	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/util/random"
)

var rng = random.New()

func main() {
	articleExample()
	//	randomExample()
}

func articleExample() {
	suite := edwards25519.NewBlakeSHA256Ed25519()

	var G kyber.Point = suite.Point().Base() //suite.Point().Pick(rng)
	someRandomScalar := suite.Scalar().SetInt64(271210349)
	var H kyber.Point = suite.Point().Mul(someRandomScalar, G) //suite.Point().Pick(rng)

	fmt.Printf("Curve points:\n G:\t%s\n H:\t%s\n\n", G, H)

	//blinding factor + amount curve point TxIN1 from the article example (a=10, r=14): 14*G, 10*H
	r_i1 := suite.Scalar().SetInt64(14)
	a_i1 := suite.Scalar().SetInt64(10)
	riG1 := suite.Point().Mul(r_i1, G)
	aiH1 := suite.Point().Mul(a_i1, H)

	//TxIN2 from the article example (a=30, r=85): 85*G, 30*H
	r_i2 := suite.Scalar().SetInt64(85)
	a_i2 := suite.Scalar().SetInt64(30)
	riG2 := suite.Point().Mul(r_i2, G)
	aiH2 := suite.Point().Mul(a_i2, H)

	//TxIN3 from the article example (a=10, r=43): 43*G, 10*H
	r_i3 := suite.Scalar().SetInt64(45)
	a_i3 := suite.Scalar().SetInt64(10)
	riG3 := suite.Point().Mul(r_i3, G)
	aiH3 := suite.Point().Mul(a_i3, H)

	//calculate pedersen EC commitments for the TxIN's
	//TxIN1: c=14*G+10*H
	c_i1 := suite.Point().Add(riG1, aiH1)
	//TxIN2: c=85*G+30*H
	c_i2 := suite.Point().Add(riG2, aiH2)
	//TxIN3: c=43*G+10*H
	c_i3 := suite.Point().Add(riG3, aiH3)
	//print them out for comparison
	fmt.Printf("c_i1: %s\n", c_i1)
	fmt.Printf("c_i2: %s\n", c_i2)
	fmt.Printf("c_i3: %s\n", c_i3)
	fmt.Printf("\n")

	//combined commitment for all TxIN's together
	c_all_i := suite.Point().Add(c_i1, c_i2)
	c_all_i = suite.Point().Add(c_all_i, c_i3)
	fmt.Printf("c_all_i: %s\n", c_all_i)

	//calculate c_all_i by summing all curve points separately,
	//to see the result is the same and the EC math works as I expected
	c_all_i_2 := suite.Point().Add(riG1, aiH1)
	c_all_i_2 = suite.Point().Add(c_all_i_2, riG2)
	c_all_i_2 = suite.Point().Add(c_all_i_2, aiH2)
	c_all_i_2 = suite.Point().Add(c_all_i_2, riG3)
	c_all_i_2 = suite.Point().Add(c_all_i_2, aiH3)
	fmt.Printf("c_all_i_2: %s\n", c_all_i_2)

	//blinding factor and curve point for TxOUT1 from the article example (a=40, r=28): 28*G, 40*H
	r_o1 := suite.Scalar().SetInt64(28)
	a_o1 := suite.Scalar().SetInt64(40)
	roG1 := suite.Point().Mul(r_o1, G)
	voH1 := suite.Point().Mul(a_o1, H)
	c_o1 := suite.Point().Add(roG1, voH1)

	//TxOUT2 from the article example (a=8, r=33): 33*G, 8*H
	r_o2 := suite.Scalar().SetInt64(33)
	a_o2 := suite.Scalar().SetInt64(8)
	roG2 := suite.Point().Mul(r_o2, G)
	voH2 := suite.Point().Mul(a_o2, H)
	c_o2 := suite.Point().Add(roG2, voH2)

	//TxOUT3, a.k.a the TxOUT for the fee, (a=2, r=83): 83*G, 2*H
	//the 83 is calculated in the following as the diff between input and output G
	r_total_i := suite.Scalar().Add(r_i1, r_i2)
	r_total_i = suite.Scalar().Add(r_total_i, r_i3)
	r_total_o := suite.Scalar().Add(r_o1, r_o2)
	r_fee := suite.Scalar().Sub(r_total_i, r_total_o) //this should equal 83*G
	a_fee := suite.Scalar().SetInt64(2)
	rfeeG2 := suite.Point().Mul(r_fee, G)
	afeeH2 := suite.Point().Mul(a_fee, H)
	c_fee := suite.Point().Add(rfeeG2, afeeH2)

	//try to calculate 83*G directly,
	//to compare to above difference-based way and see if it works as I expected (is the same)
	fmt.Printf("c_fee: %s\n", c_fee)
	scalar83 := suite.Scalar().SetInt64(83)
	r_83G := suite.Point().Mul(scalar83, G)
	fmt.Printf("r_fee: %s\n", r_fee)
	fmt.Printf("scalar83: %s\n", scalar83)
	fmt.Printf("c_83G: %s\n", r_83G)
	fmt.Printf("rfeeG2: %s\n", rfeeG2)

	//combined commitment for all TxOUT's together
	c_all_o := suite.Point().Add(c_o1, c_o2)
	c_all_o = suite.Point().Add(c_all_o, c_fee)

	fmt.Printf("c_o1: %s\n", c_o1)
	fmt.Printf("c_o2: %s\n", c_o2)
	fmt.Printf("c_all_o: %s\n", c_all_o)

	//calculate directly the commitment to zero, z=0*G + 0*H
	//so can compare to diff of above generated combined TxIN and TxOUT commitments
	r_z := suite.Scalar().SetInt64(0)
	a_z := suite.Scalar().SetInt64(0)
	zG := suite.Point().Mul(r_z, G)
	zH := suite.Point().Mul(a_z, H)
	c_z := suite.Point().Add(zG, zH)
	fmt.Printf("c_z: %s\n", c_z)
	//some more prints to check how point subtraction works, if interested
	//fmt.Printf("zero: %s\n", suite.Point().Sub(zG, zG))
	//fmt.Printf("zero: %s\n", suite.Point().Sub(zH, zH))
	//fmt.Printf("zero: %s\n", suite.Point().Sub(zG, zH))
	//fmt.Printf("zero: %s\n", suite.Point().Sub(zG, rfeeG2))

	//Subtract the combined commitment for all TxOUT's from the combined commitment for TxIN's
	//if the EC math done above works as expected, this should equal the commitment to zero from above
	//which is what I called the ZKP in the article
	c_compare := suite.Point().Sub(c_all_i, c_all_o)
	fmt.Printf("c_c: %s\n", c_compare)
}

//this is the same as the above article example, but using random base points and different values
func randomExample() {
	suite := edwards25519.NewBlakeSHA256Ed25519()

	var input_coins1 int64
	var input_coins2 int64
	var fee int64
	var total_input int64
	var total_output int64
	var output_coins1 int64
	var output_coins2 int64

	input_coins1 = 15
	input_coins2 = 55
	total_input = input_coins1 + input_coins2

	output_coins1 = 22
	fee = 2
	output_coins2 = total_input - fee - output_coins1
	total_output = output_coins1 + output_coins2
	fmt.Printf("Total input:%s, Total output:%s\n\n", total_input, total_output)

	G := suite.Point().Pick(rng)
	H := suite.Point().Pick(rng)

	fmt.Printf("Curve points:\n G:\t%s\n H:\t%s\n\n", G, H)

	r1 := suite.Scalar().Pick(suite.RandomStream())
	v1 := suite.Scalar().SetInt64(input_coins1)
	rG1 := suite.Point().Mul(r1, G)
	vH1 := suite.Point().Mul(v1, H)

	r2 := suite.Scalar().Pick(suite.RandomStream())
	v2 := suite.Scalar().SetInt64(input_coins2)
	rG2 := suite.Point().Mul(r2, G)
	vH2 := suite.Point().Mul(v2, H)

	c_i1 := suite.Point().Add(rG1, vH1)
	c_i2 := suite.Point().Add(rG2, vH2)
	fmt.Printf("c_i1: %s\n", c_i1)
	fmt.Printf("c_i2: %s\n", c_i2)
	fmt.Printf("\n")

	c_all_i := suite.Point().Add(c_i1, c_i2)
	fmt.Printf("c_all_i: %s\n", c_all_i)

	c_all_i_2 := suite.Point().Add(rG1, vH1)
	c_all_i_2 = suite.Point().Add(c_all_i_2, rG2)
	c_all_i_2 = suite.Point().Add(c_all_i_2, vH2)
	fmt.Printf("c_all_i_2: %s\n", c_all_i_2)

	r_o1 := suite.Scalar().Pick(suite.RandomStream())
	v_o1 := suite.Scalar().SetInt64(output_coins1)
	roG1 := suite.Point().Mul(r_o1, G)
	voH1 := suite.Point().Mul(v_o1, H)
	c_o1 := suite.Point().Add(roG1, voH1)

	r_o2 := suite.Scalar().Pick(suite.RandomStream())
	v_o2 := suite.Scalar().SetInt64(output_coins2)
	roG2 := suite.Point().Mul(r_o2, G)
	voH2 := suite.Point().Mul(v_o2, H)
	c_o2 := suite.Point().Add(roG2, voH2)

	//	r_fee := suite.Scalar().SetInt64(total_input-total_output)
	r_total_i := suite.Scalar().Add(r1, r2)
	r_total_o := suite.Scalar().Add(r_o1, r_o2)
	r_fee := suite.Scalar().Sub(r_total_i, r_total_o)
	v_fee := suite.Scalar().SetInt64(fee)
	rfeeG2 := suite.Point().Mul(r_fee, G)
	vfeeH2 := suite.Point().Mul(v_fee, H)
	c_fee := suite.Point().Add(rfeeG2, vfeeH2)

	c_all_o := suite.Point().Add(c_o1, c_o2)
	c_all_o = suite.Point().Add(c_all_o, c_fee)

	fmt.Printf("c_o1: %s\n", c_o1)
	fmt.Printf("c_o2: %s\n", c_o2)
	fmt.Printf("c_all_o: %s\n", c_all_o)

	r_z := suite.Scalar().SetInt64(0)
	v_z := suite.Scalar().SetInt64(0)
	zG := suite.Point().Mul(r_z, G)
	zH := suite.Point().Mul(v_z, H)
	c_z := suite.Point().Add(zG, zH)
	fmt.Printf("c_z: %s\n", c_z)

	c_compare := suite.Point().Sub(c_all_i, c_all_o)
	fmt.Printf("c_c: %s\n", c_compare)
}
