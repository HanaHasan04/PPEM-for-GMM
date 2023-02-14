package main

import (
	"fmt"

	"github.com/tuneinsight/lattigo/v4/ckks"
	"github.com/tuneinsight/lattigo/v4/rlwe"
)

func main() {
	// define the number of parties and the data for each party
	N := 3
	x := make([][]float64, N)
	for i := 0; i < N; i++ {
		x[i] = []float64{float64(i)}
	}

	// set up the CKKS parameters and create a context
	params := ckks.DefaultParams[ckks.PN12QP109]
	params.Scale = 1 << 40
	params.SetScale()
	context := ckks.NewContextWithParams(params)

	// create a CKKS encoder
	encoder := ckks.NewEncoder(context)

	// create a slice to hold the encrypted data for each party
	encX := make([]*ckks.Ciphertext, N)

	// encrypt the data for each party
	for i := 0; i < N; i++ {
		plaintext := encoder.EncodeNew(x[i], context.MaxSlots())
		ciphertext := ckks.NewCiphertext(context, 1, context.Levels()-1)
		context.Encrypt(ciphertext, plaintext, rlwe.GaussianSampler)
		encX[i] = ciphertext
	}

	// create a slice to hold the encrypted sum
	encSum := ckks.NewCiphertext(context, 1, context.Levels()-1)

	// sum the encrypted data
	for i := 0; i < N; i++ {
		context.Add(encSum, encSum, encX[i])
	}

	// create a decryption context
	decryptor := ckks.NewDecryptor(context, context.SecretKey)

	// decrypt the sum and print the result
	plaintext := ckks.NewPlaintext(context, context.MaxSlots())
	decryptor.Decrypt(encSum, plaintext)
	result := encoder.Decode(plaintext)
	fmt.Println(result)
}
