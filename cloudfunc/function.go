package cloudfunc

import (
	"net/http"
	"strconv"

	"github.com/GoogleCloudPlatform/functions-framework-go/functions"
	"github.com/gin-gonic/gin"
)

var router *gin.Engine

func init() {
	gin.SetMode(gin.ReleaseMode)
	router = gin.Default()
	router.GET("/", intro)
	router.GET("/gcd", getGcd)
	router.GET("/powmod", getPowMod)
	router.GET("/extgcd", getExtGcd)
	router.GET("/modinv", getModInv)
	router.Run()
	functions.HTTP("LazyCrypto", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	router.ServeHTTP(w, r)
}

func intro(c *gin.Context) {
	c.String(
		http.StatusOK,
		`
1. /gcd?a=3&b=5         ==> Calculate the gcd of 3 and 5
2. /powmod?a=3&b=5&p=7  ==> Calculate 3^5 mod 7 using quickpow
3. /extgcd?a=3&b=5      ==> Calculate the extended gcd of 3 and 5
4. /modinv?a=3&b=5      ==> Calculate the modular inverse of 3 mod 5
`,
	)
}

func gcd(a, b int) int {
	if b == 0 {
		return a
	}
	return gcd(b, a%b)
}

func getGcd(c *gin.Context) {
	a, errA := strconv.Atoi(c.Query("a"))
	b, errB := strconv.Atoi(c.Query("b"))
	if errA != nil || errB != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"message": "Wrong params",
		})
	}
	c.JSON(http.StatusOK, gin.H{
		"result": gcd(a, b),
	})
}

func powMod(a, b, p int) int {
	ret := 1
	for b != 0 {
		if b&1 != 0 {
			ret = (ret * a) % p
		}
		a = (a * a) % p
		b >>= 1
	}

	return ret
}

func getPowMod(c *gin.Context) {
	a, errA := strconv.Atoi(c.Query("a"))
	b, errB := strconv.Atoi(c.Query("b"))
	p, errP := strconv.Atoi(c.Query("p"))
	if errA != nil || errB != nil || errP != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"message": "Wrong params",
		})
	}
	c.JSON(http.StatusOK, gin.H{
		"result": powMod(a, b, p),
	})
}

func extGcd(a, b int) (int, int, int) {
	if b == 0 {
		return a, 1, 0
	}
	d, y, x := extGcd(b, a%b)
	y -= a / b * x
	return d, x, y
}

func getExtGcd(c *gin.Context) {
	a, errA := strconv.Atoi(c.Query("a"))
	b, errB := strconv.Atoi(c.Query("b"))
	if errA != nil || errB != nil {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"message": "Wrong params",
		})
	}
	d, x, y := extGcd(a, b)
	c.JSON(http.StatusOK, gin.H{
		"d": d,
		"x": x,
		"y": y,
	})
}

// a > 0
func modInv(a, n int) int {
	d, _, y := extGcd(n, a)
	if d != 1 {
		return -1
	}
	return y % n
}

func getModInv(c *gin.Context) {
	a, errA := strconv.Atoi(c.Query("a"))
	b, errB := strconv.Atoi(c.Query("b"))
	if errA != nil || errB != nil || a <= 0 {
		c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{
			"message": "Wrong params (a must be positive)",
		})
	}
	c.JSON(http.StatusOK, gin.H{
		"result": modInv(a, b),
	})
}
