package main

import (
	"fmt"
	"math/rand"

	//"github.com/ldsec/lattigo/v2/dckks"

	"github.com/tuneinsight/lattigo/v4/ckks"
	"github.com/tuneinsight/lattigo/v4/rlwe"
)

func main() {
	// Set up the encryption parameters
	params, err := ckks.NewParametersFromLiteral(2, 50, 0, 0, 3.2, 2, 0)
	if err != nil {
		panic(err)
	}

	// Set the number of parties
	N := 3

	// Generate the public and private keys for each party
	sks := make([]*rlwe.SecretKey, N)
	pks := make([]*rlwe.PublicKey, N)
	for i := 0; i < N; i++ {
		keygen := ckks.NewKeyGenerator(params)
		sk, pk := keygen.GenKeyPair()
		sks[i] = sk
		pks[i] = pk
	}

	// Encrypt each party's private data
	plaintexts := make([][]complex128, N)
	ciphertexts := make([][]*rlwe.Ciphertext, N)
	for i := 0; i < N; i++ {
		plaintexts[i] = make([]complex128, params.Slots())
		for j := 0; j < params.Slots(); j++ {
			plaintexts[i][j] = complex(rand.Float64(), 0)
		}
		ciphertexts[i] = keygen.Encrypt(plaintexts[i], pks[i])
	}

	// Homomorphically add the encrypted values together
	encryptedSum := ciphertexts[0]
	for i := 1; i < N; i++ {
		encryptedSum = keygen.Add(encryptedSum, ciphertexts[i])
	}

	// Decrypt the sum to get the result
	decryptor := ckks.NewDecryptor(params, sks[0])
	decryptedSum := decryptor.Decrypt(encryptedSum)

	// Print the result
	fmt.Println("Sum of private values:", decryptedSum[0])
}
