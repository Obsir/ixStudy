//打开字滑入效果
window.onload = function () {
    $(".connect p").eq(0).animate({"left": "0%"}, 600);
    $(".connect p").eq(1).animate({"left": "0%"}, 400);
};
//jquery.validate表单验证
$(document).ready(function () {

    //登陆表单验证
    $("#loginForm").validate({
        rules: {
            username: {
                required: true, // 必填
                minlength: 3, // 最少6个字符
                maxlength: 32, // 最多20个字符
            },
            password: {
                required: true,
                minlength: 3,
                maxlength: 32,
            },
        },
        //错误信息提示
        messages: {
            username: {
                required: "必须填写用户名",
                minlength: "用户名至少为3个字符",
                maxlength: "用户名至多为32个字符",
                remote: "用户名已存在",
            },
            password: {
                required: "必须填写密码",
                minlength: "密码至少为3个字符",
                maxlength: "密码至多为32个字符",
            },
        },

    });
    //注册表单验证
    $("#registerForm").validate({
        rules: {
            username: {
                required: true, // 是否必填
                minlength: 3, // 最少6个字符
                maxlength: 32, // 最多32个字符
                // remote: {
                // 	// 这个地址，是当注册页面填完用户名时，
                // 	// 直接请求后端，看你填写的帐号是否已经是老用户/被注册过的意思，
                // 	// 如果后端没有做校验，则不需要这个。
                // 	url: "http://xxxxx/xxx",
                // 	type: "post",
                // },
            },
            password: {
                required: true,
                minlength: 3,
                maxlength: 32,
            },
            email: {
                required: true,
                email: true,
            },
            re_password: {
                required: true,
                minlength: 3,
                equalTo: '.password'
            },
            phone: {
                required: true,
                phone_number: true, // 自定义的规则
                digits: true, // 整数
            }
        },
        // 错误信息提示
        messages: {
            username: {
                required: "必须填写用户名",
                minlength: "用户名至少为3个字符",
                maxlength: "用户名至多为32个字符",
                remote: "用户名已存在",
            },
            password: {
                required: "必须填写密码",
                minlength: "密码至少为3个字符",
                maxlength: "密码至多为32个字符",
            },
            email: {
                required: "请输入邮箱地址",
                email: "请输入正确的email地址"
            },
            re_password: {
                required: "请再次输入密码",
                minlength: "确认密码不能少于3个字符",
                equalTo: "两次输入密码不一致", // 与另一个元素相同
            },
            position: {
                required: "请输入职位",
            },
            company: {
                required: "请选择公司"
            },
            phone: {
                required: "请输入手机号码",
                digits: "请输入正确的手机号码",
            },

        },
    });
    // 添加自定义验证规则
    jQuery.validator.addMethod("phone", function (value, element) {
        var phone_length = value.length;
        // 手机号正则表达式（其实这个已经很旧了，现在手机号1开头，11位数字就差不多了。）
        var phone_reg = /^(((13[0-9]{1})|(15[0-9]{1}))+\d{8})$/
        return this.optional(element) || (phone_length == 11 && phone_reg.test(value));
    }, "手机号码格式错误");

    // 发起登录、注册请求，这里没写，
    // 一种是通过 type="submit" 提交表格数据，
    // 另一种是在当前页面发起 $.ajax 请求。
});
