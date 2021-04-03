package main

//https://docs.grin.mw/wiki/introduction/mimblewimble/commitments/

import (
	"fmt"
	"go.dedis.ch/kyber/v3/group/edwards25519"
	"go.dedis.ch/kyber/v3/util/random"
)

var rng = random.New()

func main() {
	suite := edwards25519.NewBlakeSHA256Ed25519()

	var input_coins1 int64
	var input_coins2 int64
	var fee int64
	var total_input int64
	var total_output int64
	var output_coins1 int64
	var output_coins2 int64

	input_coins1 =15
	input_coins2 =55
	total_input = input_coins1+input_coins2

	output_coins1 = 22
	fee = 2
	output_coins2 = total_input - fee - output_coins1
	total_output = output_coins1 + output_coins2
	fmt.Printf("Total input:%s, Total output:%s\n\n",total_input,total_output)

	G := suite.Point().Pick(rng)
	H := suite.Point().Pick(rng)

	fmt.Printf("Curve points:\n G:\t%s\n H:\t%s\n\n",G,H)

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

